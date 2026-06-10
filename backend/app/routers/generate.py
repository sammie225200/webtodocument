from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import get_db
from app.models import Site
from app.auth import get_current_user

router = APIRouter(
    prefix="/api/generate",
    tags=["Generate"]
)


@router.get("/")
def generate_status():
    return {
        "status": "ok",
        "message": "Generate endpoint working"
    }


@router.post("/")
async def generate_website(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        content = await file.read()

        file_id = str(uuid4())

        site = Site(
            user_id=current_user["id"],
            file_id=file_id,
            template="modern",
            status="generated",
            preview_url=f"/api/generate/preview/{file_id}",
            download_url=f"/api/generate/download/{file_id}",
            generation_time=0.0,
        )

        db.add(site)
        db.commit()
        db.refresh(site)

        return {
            "success": True,
            "site_id": site.id,
            "file_id": file_id,
            "preview_url": site.preview_url,
            "download_url": site.download_url,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/preview/{file_id}")
def preview_site(
    file_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "file_id": file_id,
        "message": "Preview endpoint working"
    }


@router.get("/download/{file_id}")
def download_site(
    file_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "file_id": file_id,
        "message": "Download endpoint working"
    }