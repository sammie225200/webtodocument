from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Site

router = APIRouter(
    tags=["Sites"]
)


@router.get("/sites")
def list_sites(
    db: Session = Depends(get_db)
):
    return db.query(Site).all()


@router.get("/sites/{file_id}")
def get_site(
    file_id: str,
    db: Session = Depends(get_db)
):
    site = (
        db.query(Site)
        .filter(Site.file_id == file_id)
        .first()
    )

    if not site:
        raise HTTPException(
            404,
            "Site not found"
        )

    return site


@router.delete("/sites/{file_id}")
def delete_site(
    file_id: str,
    db: Session = Depends(get_db)
):
    site = (
        db.query(Site)
        .filter(Site.file_id == file_id)
        .first()
    )

    if not site:
        raise HTTPException(
            404,
            "Site not found"
        )

    db.delete(site)
    db.commit()

    return {
        "success": True
    }