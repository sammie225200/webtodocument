from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)
from sqlalchemy.sql import func

from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, nullable=False)

    file_id = Column(String, unique=True, nullable=False)

    slug = Column(String)

    template = Column(String)

    status = Column(String, default="generated")

    preview_url = Column(String)

    download_url = Column(String)

    published_url = Column(String)

    generation_time = Column(Float)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    file_id = Column(String)

    rating = Column(Integer)

    comment = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    supabase_id = Column(
        String,
        unique=True,
        nullable=False
    )

    role = Column(
        String,
        default="user"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )