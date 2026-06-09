from fastapi import APIRouter, HTTPException

from app.schemas import SignupRequest, LoginRequest
from app.supabase_client import supabase

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
async def signup(data: SignupRequest):
    try:
        result = supabase.auth.admin.create_user(
            {
                "email": data.email,
                "password": data.password,
                "email_confirm": True
            }
        )

        return {
            "success": True,
            "user_id": result.user.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
async def login(data: LoginRequest):
    try:
        result = supabase.auth.sign_in_with_password(
            {
                "email": data.email,
                "password": data.password
            }
        )

        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "user_id": result.user.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )