import os
import sys
import uvicorn
from pathlib import Path

# Dodaj katalog 'app' do PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

if __name__ == "__main__":
    port = 8000
    max_retries = 5

    for attempt in range(max_retries):
        try:
            print(f"[INFO] Próba uruchomienia na porcie {port}...")
            uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
            break
        except OSError as e:
            if "10048" in str(e) or "address already in use" in str(e).lower():
                print(f"[WARNING] Port {port} zajęty, próbuję {port + 1}...")
                port += 1
            else:
                raise
    else:
        print(f"[ERROR] Nie udało się uruchomić backendu po {max_retries} próbach")
        sys.exit(1)
