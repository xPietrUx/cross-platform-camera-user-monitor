from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from typing import List
from sqlmodel import Session, select
from services import video_processor
from db.database import get_session
from db.models import FocusLog, User, DistractionStat
from collections import defaultdict
from datetime import datetime, timedelta

# Importujemy zależność z nowego pliku
from dependencies import get_current_user

router = APIRouter()


@router.get("/cameras", response_model=List[dict])
def get_cameras():
    # Zwraca listę dostępnych kamer w systemie.
    return [
        {"id": "cam1", "name": "Zintegrowana kamera"},
        {"id": "cam2", "name": "Kamera USB"},
    ]


@router.post("/cameras/select")
def select_camera():
    # Pozwala wybrać kamerę, która będzie używana do śledzenia.
    return {"message": "Wybrano kamerę: cam1"}


@router.get("/stream")
def video_stream(current_user: User = Depends(get_current_user)):
    """
    Endpoint do streamingu. Wymaga tokena (przekazywanego w URL ?token=...).
    Przekazuje ID użytkownika do procesora wideo.
    """
    try:
        return StreamingResponse(
            # Przekazujemy ID zalogowanego użytkownika
            video_processor.generate_frames(user_id=current_user.id),
            media_type="multipart/x-mixed-replace; boundary=frame",
        )
    except RuntimeError as e:
        return {"error": str(e)}


@router.get("/stats")
def get_video_stats():
    """
    Zwraca aktualne statystyki analizy wideo (np. poziom skupienia).
    """
    stats = video_processor.get_focus_stats()
    return {"is_focused": stats["is_focused"], "focus_score": stats["focus_score"]}


@router.get("/history")
def get_focus_history(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Zwraca historię skupienia TYLKO dla zalogowanego użytkownika.
    """
    # Filtrujemy po user_id, pobieramy ostatnie 8 wpisów
    statement = (
        select(FocusLog)
        .where(FocusLog.user_id == current_user.id)
        .order_by(FocusLog.timestamp.desc())
        .limit(8)
    )
    results = session.exec(statement).all()

    labels = []
    values = []

    # Odwracamy kolejność, aby na wykresie czas płynął od lewej do prawej
    for log in reversed(results):
        labels.append(log.timestamp.strftime("%H:%M"))
        values.append(log.focus_score)

    return {"labels": labels, "datasets": [{"name": "Skupienie", "values": values}]}


@router.get("/stats/daily")
def get_daily_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Zwraca średni poziom skupienia z ostatnich 7 dni.
    """
    # 1. Przygotuj zakres dat (ostatnie 7 dni)
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]

    # 2. Pobierz logi z bazy dla tego użytkownika z ostatnich 7 dni
    start_date = dates[0]
    statement = (
        select(FocusLog)
        .where(FocusLog.user_id == current_user.id)
        .where(FocusLog.timestamp >= start_date)
    )
    logs = session.exec(statement).all()

    # 3. Pogrupuj wyniki po dacie
    grouped_data = defaultdict(list)
    for log in logs:
        log_date = log.timestamp.date()
        grouped_data[log_date].append(log.focus_score)

    # 4. Oblicz średnie i przygotuj etykiety
    labels = []
    values = []

    # Słownik do tłumaczenia dni tygodnia na polski
    days_map = {
        0: "Pon",
        1: "Wt",
        2: "Śr",
        3: "Czw",
        4: "Pt",
        5: "Sob",
        6: "Ndz",
    }

    for date in dates:
        # Etykieta: Dzień tygodnia (np. "Pon")
        day_name = days_map[date.weekday()]
        labels.append(day_name)

        # Wartość: Średnia lub 0 jeśli brak danych
        scores = grouped_data[date]
        if scores:
            avg_score = int(sum(scores) / len(scores))
            values.append(avg_score)
        else:
            values.append(0)

    return {
        "labels": labels,
        "datasets": [{"name": "Średnie skupienie (%)", "values": values}],
    }


@router.get("/stats/distractions")
def get_distraction_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Zwraca sumę rozproszeń z dzisiejszego dnia (zapisane + bieżące).
    """
    today = datetime.now().date()

    # 1. Pobierz dane zapisane w bazie (z poprzednich godzin dzisiaj)
    statement = select(DistractionStat).where(
        DistractionStat.user_id == current_user.id, DistractionStat.date == today
    )
    stats = session.exec(statement).all()

    totals = {"absent": 0, "looking_away": 0, "multiple_faces": 0}

    for stat in stats:
        if stat.distraction_type in totals:
            totals[stat.distraction_type] += stat.count

    # 2. Dodaj dane "na żywo" z obecnej godziny (z pamięci RAM)
    live_stats = video_processor.get_current_user_distractions(current_user.id)

    totals["absent"] += live_stats["absent"]
    totals["looking_away"] += live_stats["looking_away"]
    totals["multiple_faces"] += live_stats["multiple_faces"]

    # Formatowanie dla wykresu
    return {
        "labels": ["Brak obecności", "Odwrócenie wzroku", "Inne osoby"],
        "datasets": [
            {
                "name": "Rozproszenia",
                "values": [
                    totals["absent"],
                    totals["looking_away"],
                    totals["multiple_faces"],
                ],
            }
        ],
    }


@router.get("/stats/activity")
def get_activity_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Zwraca sumę punktów skupienia dla każdego dnia z ostatnich 7 dni.
    Pozwala to oszacować, w który dzień użytkownik włożył najwięcej wysiłku.
    """
    # 1. Zakres dat (ostatnie 7 dni)
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]

    start_date = dates[0]
    statement = (
        select(FocusLog)
        .where(FocusLog.user_id == current_user.id)
        .where(FocusLog.timestamp >= start_date)
    )
    logs = session.exec(statement).all()

    # 2. Sumujemy wyniki dla każdego dnia
    grouped_data = defaultdict(int)  # Domyślnie 0
    for log in logs:
        log_date = log.timestamp.date()
        # Dodajemy wynik do sumy dnia (np. 85 + 90 + 100...)
        # To uwzględnia zarówno czas pracy (więcej wpisów) jak i jakość (wyższy wynik)
        grouped_data[log_date] += log.focus_score

    labels = []
    values = []

    days_map = {
        0: "Poniedziałek",
        1: "Wtorek",
        2: "Środa",
        3: "Czwartek",
        4: "Piątek",
        5: "Sobota",
        6: "Niedziela",
    }

    for date in dates:
        day_name = days_map[date.weekday()]
        total_score = grouped_data[date]

        # Dodajemy do wykresu tylko dni, w których była jakakolwiek aktywność
        # (żeby wykres kołowy nie miał pustych sekcji)
        if total_score > 0:
            labels.append(day_name)
            values.append(total_score)

    return {
        "labels": labels,
        "datasets": [{"name": "Wkład pracy", "values": values}],
    }
