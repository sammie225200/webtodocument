from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException
)

from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["Preview"]
)

GENERATED_DIR = Path("generated")


@router.get(
    "/preview/{file_id}",
    response_class=HTMLResponse
)
def preview(
    file_id: str
):
    file_path = GENERATED_DIR / f"{file_id}.html"

    if not file_path.exists():
        raise HTTPException(
            404,
            "Site not found"
        )

    return file_path.read_text(
        encoding="utf-8"
    )