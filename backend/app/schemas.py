from pydantic import (
    BaseModel,
    EmailStr
)


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GenerateResponse(BaseModel):
    success: bool
    file_id: str
    preview_url: str
    download_url: str


class PublishRequest(BaseModel):
    slug: str


class FeedbackRequest(BaseModel):
    file_id: str
    rating: int
    comment: str | None = None