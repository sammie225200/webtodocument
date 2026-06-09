from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Site,
    Feedback,
    User
)

router = APIRouter(
    tags=["Admin"]
)


@router.get("/admin/metrics")
def metrics(
    db: Session = Depends(get_db)
):

    return {
        "users":
            db.query(User).count(),

        "sites":
            db.query(Site).count(),

        "feedback":
            db.query(Feedback).count()
    }