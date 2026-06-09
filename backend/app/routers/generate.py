import uuid
import time

from pathlib import Path
from app.auth import get_current_user
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Site
from app.schemas import GenerateResponse

from app.services.document_parser import parse_document
from app.services.mistral_service import generate_website

router = APIRouter(tags=["Generate"])

GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)


@router.post(
    "/generate",
    response_model=GenerateResponse
)
async def generate(
    document: UploadFile = File(...),
    prompt: str = Form(""),
    template: str = Form("modern"),
    db: Session = Depends(get_db)
):
    try:

        start = time.time()

        content = await document.read()

        document_text = parse_document(
            document.filename,
            content
        )

        html = generate_website(
            document_text,
            prompt,
            template
        )

        file_id = str(uuid.uuid4())

        html_path = GENERATED_DIR / f"{file_id}.html"

        html_path.write_text(
            html,
            encoding="utf-8"
        )

        generation_time = round(
            time.time() - start,
            2
        )

        site = Site(
            user_id=None,
            file_id=file_id,
            template=template,
            status="generated",
            preview_url=f"/api/preview/{file_id}",
            download_url=f"/api/download/{file_id}",
            generation_time=generation_time
        )

        db.add(site)
        db.commit()

        return GenerateResponse(
            success=True,
            file_id=file_id,
            preview_url=f"/api/preview/{file_id}",
            download_url=f"/api/download/{file_id}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )