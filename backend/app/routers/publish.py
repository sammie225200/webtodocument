import shutil

from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException
)

router = APIRouter(
    tags=["Publish"]
)

GENERATED_DIR = Path("generated")
PUBLISHED_DIR = Path("published")

PUBLISHED_DIR.mkdir(
    exist_ok=True
)


@router.post("/publish/{file_id}")
def publish(
    file_id: str
):

    source = GENERATED_DIR / f"{file_id}.html"

    if not source.exists():
        raise HTTPException(
            404,
            "File not found"
        )

    destination = (
        PUBLISHED_DIR /
        f"{file_id}.html"
    )

    shutil.copy(
        source,
        destination
    )

    return {
        "success": True,
        "url": f"/published/{file_id}.html"
    }