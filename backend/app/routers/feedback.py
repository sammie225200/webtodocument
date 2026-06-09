from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Feedback
from app.schemas import FeedbackRequest

router = APIRouter(
    tags=["Feedback"]
)


@router.post("/feedback")
def submit_feedback(
    data: FeedbackRequest,
    db: Session = Depends(get_db)
):

    feedback = Feedback(
        file_id=data.file_id,
        rating=data.rating,
        comment=data.comment
    )

    db.add(feedback)
    db.commit()

    return {
        "success": True
    }