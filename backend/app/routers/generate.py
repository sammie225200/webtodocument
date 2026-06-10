from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import tempfile
import uuid
import time

from app.database import get_db
from app.models import Site
from app.auth import get_current_user

router = APIRouter(
    prefix="/api/generate",
    tags=["Website Generation"]
)

# Vercel-safe temp directory
GENERATED_DIR = Path(tempfile.gettempdir()) / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


@router.post("")
async def generate_website_endpoint(
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Generate website from uploaded content.
    """

    start_time = time.time()

    file_id = str(uuid.uuid4())

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated Website</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: auto;
                padding: 40px;
            }}
        </style>
    </head>
    <body>
        <h1>Generated Website</h1>
        <p>Generated from Document-to-Website platform.</p>
    </body>
    </html>
    """

    output_file = GENERATED_DIR / f"{file_id}.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    generation_time = round(time.time() - start_time, 2)

    site = Site(
        user_id=current_user.id,
        file_id=file_id,
        template="modern",
        status="generated",
        generation_time=generation_time,
        preview_url=f"/api/generate/preview/{file_id}",
        download_url=f"/api/generate/download/{file_id}",
        published_url=None
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
        "generation_time": generation_time
    }


@router.get("/preview/{file_id}")
async def preview_site(file_id: str):

    file_path = GENERATED_DIR / f"{file_id}.html"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Generated file not found"
        )

    return {
        "file_id": file_id,
        "html": file_path.read_text(encoding="utf-8")
    }


@router.get("/download/{file_id}")
async def download_site(file_id: str):

    file_path = GENERATED_DIR / f"{file_id}.html"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Generated file not found"
        )

    return {
        "file_id": file_id,
        "content": file_path.read_text(encoding="utf-8")
    }


@router.get("/my-sites")
async def my_sites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    sites = (
        db.query(Site)
        .filter(Site.user_id == current_user.id)
        .all()
    )

    return sites