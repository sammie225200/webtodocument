from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import Site

router = APIRouter(
    prefix="/api/publish",
    tags=["Publish"]
)


@router.get("/")
def publish_status():
    return {
        "status": "ok",
        "message": "Publish router working"
    }


@router.post("/{site_id}")
def publish_site(
    site_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(
        Site.id == site_id
    ).first()

    if not site:
        raise HTTPException(
            status_code=404,
            detail="Site not found"
        )

    site.status = "published"
    db.commit()

    return {
        "success": True,
        "site_id": site.id,
        "status": site.status
    }