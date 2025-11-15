import cv2
import time


def generate_frames():
    """
    Generator przechwytujący klatki z kamery w pętli
    i zwraca je w formacie 'streamingu'
    """

    # TODO: Dać wybór użytkownikowi z której kamery chce korzystać
    cap = cv2.VideoCapture(0)

    # TODO: Zebrać informacje o rozdzielczości kamery i odświeżanie
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    cap.set(cv2.CAP_PROP_FPS, 60)

    if not cap.isOpened():
        raise RuntimeError("Nie można otworzyć kamery")

    try:
        while True:
            # Odczytanie klatki z kamery
            success, frame = cap.read()
            if not success:
                break

            # Zakodowanie klatki do formatu JPEG
            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            # Zwracanie klatki w formacie multipart - możliwość strumieniowania do przeglądarki
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

            # Opóźnienie by kontrolować liczbę klatek na sekundę
            time.sleep(1 / 60)

    finally:
        # Upewnienie, że kamera zostanie zwolniona po zakończeniu procesu
        cap.release()
