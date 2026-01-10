# Krok po kroku wdrożenie

Aby zainicjalizować projekt, terminalu (`CTRL+~`):

```bash
cd backend
pip install -r requirements.txt
```

# Uruchomienie Backend

Terminal:

```bash
cd app
fastapi dev main.py
```

# Dokumentacja

https://fastapi.tiangolo.com/#create-it

# Budowanie appki

```bash
# 1. Skopiuj kaskady Haar (tylko przy pierwszym buildzie)
mkdir haarcascades
copy "$(python -c 'import cv2; print(cv2.data.haarcascades)')haarcascade_frontalface_default.xml" haarcascades\
copy "$(python -c 'import cv2; print(cv2.data.haarcascades)')haarcascade_eye.xml" haarcascades\

# 2. Zbuduj api.exe dla win
pyinstaller --noconfirm --onefile --windowed --name api `
  --hidden-import=passlib.handlers.bcrypt `
  --add-data="haarcascades;haarcascades" `
  run_server.py --distpath dist/win
```
