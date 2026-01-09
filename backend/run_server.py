import uvicorn
import os
import sys

# Dodaj katalog bieżący do ścieżki, aby importy z 'app' i 'db' działały
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    # Uruchomienie serwera
    # workers=1 jest ważne dla PyIntallera
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)
