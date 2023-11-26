from models import *
from tortoise import fields, models
from fastapi import HTTPException, status

from enum import Enum, StrEnum
import time
import datetime
from typing import Optional

from pydantic import BaseModel

from common.cancer_types import CancerType, get_cancer_type


class Calendar(BaseModel):
    days: list["Day"] = []

class Day(BaseModel):
    month_number: int
    day_number: int
    weekday: int
    machines: list["Machine"] = []

class Machine(BaseModel):
    resource: ResourceResponse
    events: list["Event"] = []

class Event(BaseModel):
    start_hour: int
    start_minute: int
    duration: int
    appointment_id: int
    display_name: Optional[str] = None
    color: str = "#36BDAD"


async def get_calendar():
    calendar = Calendar()

    # get current month, day, weekday
    now = datetime.datetime.now()

    resources = await Resource.all()
    
    while len(calendar.days) < 30:
        weekday = now.weekday()

        day = Day(month_number=now.month, day_number=now.day, weekday=weekday)
        calendar.days.append(day)

        # get appointments for this day
        appointments = await Appointment.filter(
            start__gte=now.replace(hour=0, minute=0, second=0, microsecond=0),
            end__lte=now.replace(hour=23, minute=59, second=59, microsecond=999999)
        ).prefetch_related("demand__patient")

        # get maintenances for this day
        maintenances = await MaintenanceEvent.filter(
            day=day,
            type=EventType.MAINTENANCE
        )

        for machine in resources:
            events = []
            for appointment in appointments:
                if appointment.resource_id == machine.id:
                    event = Event(
                        start_hour=appointment.start.hour, 
                        start_minute=appointment.start.minute, 
                        duration=(appointment.end - appointment.start).seconds // 60,
                        appointment_id=appointment.id,
                        display_name=appointment.demand.patient.last_name[0:3].upper()
                    )
                    events.append(event)

            for maintenance in maintenances:
                if maintenance.resource_id == machine.id:
                    event = Event(
                        start_hour=maintenance.start_hour, 
                        start_minute=maintenance.start_minute, 
                        duration=maintenance.duration,
                        #appointment_id=maintenance.id,
                        display_name=maintenance.display_name,
                        color=maintenance.color
                    )
                    events.append(event)

            day.machines.append(Machine(
                resource=await ResourceResponse.create(machine), 
                events=events
            ))

        # increment day
        now += datetime.timedelta(days=1)
    
    return calendar
