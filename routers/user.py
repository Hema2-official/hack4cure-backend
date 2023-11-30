from fastapi import APIRouter, Depends

from models import *
from dependencies.auth import require_staff_token, Token

from typing import Annotated
import datetime

router = APIRouter(tags=["user"])

@router.get("/userappointments")
async def get_upcoming(
    token: Annotated[Token, Depends(require_staff_token)],
):
    print(token)
    return "csakesz"
