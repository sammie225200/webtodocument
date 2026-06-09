from fastapi import Header, HTTPException

from app.supabase_client import supabase


async def get_current_user(
    authorization: str = Header(...)
):
    try:

        token = authorization.replace(
            "Bearer ",
            ""
        )

        result = supabase.auth.get_user(
            token
        )

        return result.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )