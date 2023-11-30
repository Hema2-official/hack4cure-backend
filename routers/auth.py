from fastapi import APIRouter, Response, Request, HTTPException, status
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import httpx
from jose import jwt

import common.config as config
from models import Account, Gender
from common.auth import create_token, verify_password, hash_password, check_email
from common.logger import log

import time
from urllib.parse import urlencode
import secrets
import random
import os
from typing import Optional

router = APIRouter(tags=["auth"])


class AuthResponse(BaseModel):
    account_id: int


def _login(
    response: Response,
    account: Account
):
    token = create_token(account)

    response.set_cookie(
        key="token",
        value=token,
        max_age=400 * 24 * 3600, # 400 days
        httponly=True,
        samesite="none",
        secure=True,
    )


class LoginBody(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(
    response: Response, 
    body: LoginBody,
):
    check_email(body.email)
    account = await Account.get_or_none(email=body.email.lower())

    if account is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            "There is no account associated with this email."
        )
    
    if not account.password:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            "The account does not have password login set up."
            "Did you register through another provider?"
        )

    if not verify_password(body.password, account.password):
        await log(f"Login failed for account {str(account.id)} ({account.first_name} {account.last_name}).")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Wrong password.")

    _login(response, account)
    await log(f"Account {str(account.id)} ({account.first_name} {account.last_name}) logged in.")

    return AuthResponse(account_id=account.id)


async def _register(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    password: str = None,
    google_id: str = None,
    gender: Gender = None,
):
    account = Account()

    if email is not None:
        check_email(email)

        if await Account.get_or_none(email=email.lower()) is not None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already used.")
        
        account.email = email

    if password is not None:
        account.password = hash_password(password)

    if google_id is not None:
        account.google_id = google_id

    account.created_at = int(time.time())
    account.updated_at = int(time.time())
    account.first_name = first_name
    account.last_name = last_name
    account.gender = gender
    await account.save()
    await log(f"Account {str(account.id)} ({account.first_name} {account.last_name}) registered.")

    return account


class RegisterBody(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    gender: Optional[Gender]


@router.post("/register")
async def register(
    body: RegisterBody,
):
    account = await _register(
        email=body.email,
        password=body.password,
        first_name=body.first_name,
        last_name=body.last_name,
        gender=body.gender,
    )

    return AuthResponse(account_id=account.id)


@router.get("/google")
async def google_login():

    state = secrets.token_urlsafe(32)

    uri = urlencode({
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "response_type": "code",
        "scope": "openid email",
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "state": state,
        "nonce": random.randint(0, 2**32),
    })

    response = RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{uri}")

    response.set_cookie(
        key="state",
        value=state,
        max_age=60 * 10, # 10 minutes
        httponly=True,
        samesite="none",
        secure=True,
    )

    return response


@router.get("/google/callback")
async def google_callback(
    request: Request, 
    code: str, 
    state: str
):
    if state != request.cookies.get("state"):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid state.")

    # exchange code for token
    uri = urlencode({
        "code": code,
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    })

    async with httpx.AsyncClient() as client:
        r = await client.post(f"https://oauth2.googleapis.com/token?{uri}")

    if r.status_code != status.HTTP_200_OK:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid code.")
    
    data = r.json()
    token = jwt.decode(
        data["id_token"], 
        key=None,
        algorithms="HS256",
        options={
            "verify_signature": False, 
            "verify_aud": False,
            "verify_at_hash": False,
        }
    )

    account = await Account.get_or_none(google_id=token["sub"])

    if account is None:
        account = await _register(
            email=token["email"], 
            google_id=token["sub"]
        )

    if config.BRANCH is None:
        response = RedirectResponse(config.PREFIX + "/docs")
    else:
        response = RedirectResponse("https://hack4cure-2023-frontend.vercel.app/")
    
    _login(response, account)
    await log(f"Account {str(account.id)} logged in.")

    return response


@router.get("/logout")
async def logout(response: Response):
    try:
        response = RedirectResponse(
            'https://hack4cure-2023-frontend.vercel.app/login', 
            status_code=302
        )
        response.delete_cookie(
            key="token",
            samesite="none",
            secure=True,
        )
    except: 
        pass

    return response if response else "Logged out."
