import cv2
import time
from datetime import datetime
from sqlmodel import Session, select
from db.database import engine
from db.models import FocusLog, DistractionStat  # <--- Dodaj DistractionStat

# --- OPTYMALIZACJA 1: Ładowanie modeli raz (globalnie) ---
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# --- OPTYMALIZACJA 2: Globalna instancja kamery ---
global_camera = None


def get_camera_instance():
    """
    Zwraca globalną instancję kamery. Jeśli nie istnieje, tworzy ją.
    Dzięki temu nie otwieramy/zamykamy kamery przy każdym odświeżeniu strony.
    """
    global global_camera
    if global_camera is None or not global_camera.isOpened():
        # --- OPTYMALIZACJA 3: Użycie cv2.CAP_DSHOW na Windows ---
        # DirectShow jest znacznie szybszy przy starcie niż domyślny MSMF
        global_camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        global_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        global_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        global_camera.set(cv2.CAP_PROP_FPS, 30)

        if not global_camera.isOpened():
            # Fallback jeśli DSHOW nie zadziała
            global_camera = cv2.VideoCapture(0)

    return global_camera


# Rozszerzamy akumulator o liczniki rozproszeń
user_accumulators = {}


def get_user_accumulator(user_id):
    if user_id not in user_accumulators:
        user_accumulators[user_id] = {
            "current_hour": None,
            "focused_frames": 0,
            "total_frames": 0,
            # NOWE LICZNIKI (resetowane co godzinę przy zapisie)
            "dist_absent": 0,
            "dist_looking_away": 0,
            "dist_multiple_faces": 0,
        }
    return user_accumulators[user_id]


def get_current_user_distractions(user_id):
    """Zwraca bieżące (niezapisane jeszcze) liczniki rozproszeń dla użytkownika."""
    if user_id in user_accumulators:
        acc = user_accumulators[user_id]
        return {
            "absent": acc["dist_absent"],
            "looking_away": acc["dist_looking_away"],
            "multiple_faces": acc["dist_multiple_faces"],
        }
    return {"absent": 0, "looking_away": 0, "multiple_faces": 0}


# Globalne statystyki (chwilowe)
current_focus_stats = {
    "is_focused": False,
    "focus_score": 100,
    "history": [],
}


def save_hourly_stat(user_id, hour_timestamp, score):
    """Zapisuje wynik do bazy danych (Upsert)."""
    try:
        with Session(engine) as session:
            statement = select(FocusLog).where(
                FocusLog.user_id == user_id,
                FocusLog.timestamp == hour_timestamp,
            )
            existing_log = session.exec(statement).first()

            if existing_log:
                existing_log.focus_score = score
                session.add(existing_log)
            else:
                log = FocusLog(
                    timestamp=hour_timestamp, focus_score=score, user_id=user_id
                )
                session.add(log)

            session.commit()
    except Exception as e:
        print(f"[ERROR] Nie udało się zapisać raportu: {e}")


def save_distractions(user_id, log_date, absent, looking_away, multiple):
    """Aktualizuje statystyki rozproszeń w bazie dla danego dnia."""
    try:
        with Session(engine) as session:
            for d_type, count in [
                ("absent", absent),
                ("looking_away", looking_away),
                ("multiple_faces", multiple),
            ]:
                if count > 0:
                    statement = select(DistractionStat).where(
                        DistractionStat.user_id == user_id,
                        DistractionStat.date == log_date,
                        DistractionStat.distraction_type == d_type,
                    )
                    stat = session.exec(statement).first()
                    if stat:
                        stat.count += count
                        session.add(stat)
                    else:
                        new_stat = DistractionStat(
                            date=log_date,
                            user_id=user_id,
                            distraction_type=d_type,
                            count=count,
                        )
                        session.add(new_stat)
            session.commit()
    except Exception as e:
        print(f"[ERROR] Błąd zapisu rozproszeń: {e}")


def get_focus_stats():
    return current_focus_stats


def generate_frames(user_id: int):
    """
    Generator klatek wideo.
    """
    # Pobieramy otwartą już kamerę zamiast otwierać nową
    cap = get_camera_instance()

    if not cap.isOpened():
        raise RuntimeError("Nie można otworzyć kamery")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                # Jeśli nie uda się odczytać klatki, próbujemy ponownie (kamera może być zajęta)
                time.sleep(0.1)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # ZMIANA 1: Bardziej rygorystyczna detekcja twarzy (minNeighbors=8)
            # To sprawi, że profil twarzy nie będzie wykrywany jako "frontalface"
            faces = face_cascade.detectMultiScale(gray, 1.1, 8, minSize=(60, 60))

            # Domyślnie brak skupienia
            is_focused = False
            eyes_detected = 0

            # --- NOWA LOGIKA ROZPOZNAWANIA PRZYCZYNY ---
            current_distraction = None  # "absent", "looking_away", "multiple_faces" lub None (jeśli skupiony)

            if len(faces) == 0:
                current_distraction = "absent"
            elif len(faces) > 1:
                current_distraction = "multiple_faces"
            else:
                # Jest dokładnie 1 twarz
                (x, y, w, h) = faces[0]
                roi_gray = gray[y : y + h, x : x + w]
                roi_color = frame[y : y + h, x : x + w]

                # ZMIANA 2: Bardziej rygorystyczna detekcja oczu (minNeighbors=15)
                # Eliminuje fałszywe detekcje cieni jako oczu
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 15, minSize=(20, 20))
                eyes_detected = len(eyes)

                # --- RYSOWANIE ---
                # Rysowanie prostokąta wokół twarzy
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Rysowanie oczu
                # for ex, ey, ew, eh in eyes:
                #     cv2.rectangle(
                #         roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2
                #     )

                if eyes_detected > 0:
                    is_focused = True
                else:
                    current_distraction = "looking_away"

            # --- LOGIKA AGREGACJI ---
            acc = get_user_accumulator(user_id)
            now = datetime.now()
            this_hour = now.replace(minute=0, second=0, microsecond=0)

            if acc["current_hour"] is None:
                acc["current_hour"] = this_hour

            # Zliczamy klatki rozproszeń
            if current_distraction == "absent":
                acc["dist_absent"] += 1
            elif current_distraction == "looking_away":
                acc["dist_looking_away"] += 1
            elif current_distraction == "multiple_faces":
                acc["dist_multiple_faces"] += 1

            # Zapis co godzinę (lub przy zmianie godziny)
            if this_hour != acc["current_hour"]:
                total = acc["total_frames"]
                if total > 0:
                    score = int((acc["focused_frames"] / total) * 100)
                    save_hourly_stat(user_id, acc["current_hour"], score)

                    # Zapisujemy też rozproszenia
                    save_distractions(
                        user_id,
                        acc["current_hour"].date(),
                        acc["dist_absent"],
                        acc["dist_looking_away"],
                        acc["dist_multiple_faces"],
                    )

                acc["current_hour"] = this_hour
                acc["focused_frames"] = 0
                acc["total_frames"] = 0
                acc["dist_absent"] = 0
                acc["dist_looking_away"] = 0
                acc["dist_multiple_faces"] = 0

            acc["total_frames"] += 1
            if is_focused:
                acc["focused_frames"] += 1
            # ------------------------

            # Aktualizacja statystyk chwilowych (dla wykresu na żywo)
            current_focus_stats["is_focused"] = is_focused
            current_focus_stats["history"].append(1 if is_focused else 0)

            # ZMIANA 3: Mniejszy bufor historii (30 klatek = ok. 1 sekunda)
            # Dzięki temu wynik spadnie szybciej po odwróceniu głowy
            if len(current_focus_stats["history"]) > 30:
                current_focus_stats["history"].pop(0)

            if current_focus_stats["history"]:
                avg = sum(current_focus_stats["history"]) / len(
                    current_focus_stats["history"]
                )
                current_focus_stats["focus_score"] = int(avg * 100)

            # --- USUNIĘTO NAPISY ---
            # Rysowanie statusu
            # if is_focused:
            #     color = (0, 255, 0)
            #     status_text = "FOCUSED"
            # elif current_distraction == "absent":
            #     color = (0, 0, 255)
            #     status_text = "ABSENT"
            # elif current_distraction == "multiple_faces":
            #     color = (255, 0, 255)  # Fioletowy
            #     status_text = "MULTIPLE PEOPLE"
            # else:
            #     color = (0, 165, 255)
            #     status_text = "LOOKING AWAY"

            # cv2.putText(
            #     frame,
            #     f"Status: {status_text}",
            #     (10, 30),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.8,
            #     color,
            #     2,
            # )
            # cv2.putText(
            #     frame,
            #     f"Score: {current_focus_stats['focus_score']}%",
            #     (10, 70),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.8,
            #     color,
            #     2,
            # )

            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )
            # Zmniejszamy opóźnienie pętli dla płynności
            time.sleep(0.01)
    except Exception as e:
        print(f"Błąd generatora: {e}")
    finally:
        pass
