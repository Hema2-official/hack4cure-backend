from fastapi import APIRouter, HTTPException, status, Depends, Response

from models import *

from typing import Annotated, Optional

from dependencies.auth import require_account, require_staff_token, Token
from common.auth import hash_password, check_email
from common.logger import log

from routers.auth import _register

import random
import json
import random

with open("common/names.json") as f:
    names = json.load(f)

router = APIRouter(tags=["generate"])

@router.get("/patients")
async def generate(number: int, impatient_ratio: float = 0.5):
    for i in range(number):
        # gender with non-equal probabilities
        genders = ["male", "female"]
        gender = random.choice(genders)

        first_name = random.choice(names["first"][gender])
        last_name = random.choice(names["last"])

        print("new patient: " + first_name + " " + last_name + " " + gender)

        # create account
        await _register(
            email=None,
            password=None,
            first_name=first_name,
            last_name=last_name,
        )
