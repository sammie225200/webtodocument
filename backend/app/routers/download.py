from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException
)

from fastapi.responses import FileResponse

router = APIRouter(
    tags=["Download"]
)

GENERATED_DIR = Path("generated")


@router.get("/download/{file_id}")
def download(
    file_id: str
):
    file_path = GENERATED_DIR / f"{file_id}.html"

    if not file_path.exists():
        raise HTTPException(
            404,
            "File not found"
        )

    return FileResponse(
        path=file_path,
        filename=f"{file_id}.html",
        media_type="text/html"
    )