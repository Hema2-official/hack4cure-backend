from models import *
from tortoise import fields, models
from fastapi import HTTPException, status

from enum import Enum, StrEnum
import time
import datetime
from typing import Optional

from pydantic import BaseModel


class Calendar(BaseModel):
    days: list["Day"] = []

class Day(BaseModel):
    month_number: int
    day_number: int
    weekday: int
    machines: list["Event"] = []


class Event(BaseModel):
    start_hour: int
    start_minute: int
    duration: int
    document_id: int
    display_name: Optional[str] = None
    color: str


async def get_calendar():
    calendar = Calendar()

    # get current month, day, weekday
    now = datetime.datetime.now() - datetime.timedelta(days=29)

    documents = await Document.all().prefetch_related("patient")
    
    while len(calendar.days) < 30:
        weekday = now.weekday()

        day = Day(month_number=now.month, day_number=now.day, weekday=weekday)
        calendar.days.append(day)

        for document in documents:
            if document.timestamp.month == now.month and document.timestamp.day == now.day:
                event = Event(
                    start_hour=document.timestamp.hour,
                    start_minute=document.timestamp.minute,
                    duration=30,
                    document_id=document.id,
                    display_name=document.patient.last_name,
                    color="#028090",
                )
                day.machines.append(event)

        # increment day
        now += datetime.timedelta(days=1)
    
    return calendar
