from sqlalchemy.orm import Session

from app.models import (
    Site,
    Feedback
)


class AnalyticsService:

    @staticmethod
    def get_metrics(
        db: Session
    ):

        total_sites = (
            db.query(Site)
            .count()
        )

        feedback = (
            db.query(Feedback)
            .all()
        )

        avg_rating = 0

        if feedback:

            avg_rating = sum(
                item.rating
                for item in feedback
            ) / len(feedback)

        return {
            "total_sites":
            total_sites,

            "total_feedback":
            len(feedback),

            "avg_rating":
            round(avg_rating, 2)
        }