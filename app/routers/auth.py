import pyrebase

from fastapi import APIRouter, HTTPException, Request

from app.schemas.auth import User

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(user: User, request: Request):
    authenticator = request.app.authenticator
    try:
        authenticator.sign_in_with_email_and_password(user.email, user.password)
    except pyrebase.pyrebase.HTTPError as e:
        raise HTTPException(status_code=400, detail=e.args[1])
    return {"message": "Login successful"}


@router.post("/register")
async def register(user: User, request: Request):
    authenticator = request.app.authenticator
    try:
        authenticator.create_user_with_email_and_password(user.email, user.password)
    except pyrebase.pyrebase.HTTPError as e:
        raise HTTPException(status_code=400, detail=e.args[1])
    return {"message": "Registration successful"}
