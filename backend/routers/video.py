from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import List
from services import video_processor

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
def video_stream():
    """
    Endpoint do streamingu wideo na żywo z kamery.
    """
    try:
        return StreamingResponse(
            video_processor.generate_frames(),
            media_type="multipart/x-mixed-replace; boundary=frame",
        )
    except RuntimeError as e:
        return {"error": str(e)}
