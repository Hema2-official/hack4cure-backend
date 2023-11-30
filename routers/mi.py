# check pytorch version
import torch
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import *
from dependencies.auth import require_token, require_staff_token, require_account, Token
from common.cancer_types import get_cancer_type
from common.logger import log

from typing import Annotated, Optional
import datetime


router = APIRouter(tags=["mi"])

@router.get("")
async def get_version():
    return torch.__version__