from fastapi import APIRouter, Response, Request, HTTPException, status, Depends

from models import *
from dependencies.auth import *
from common.pdf import pdf_to_parts, parts_to_raw

from typing import Annotated


router = APIRouter(tags=["debug"])

# here should go wrappers of common functions that should be tested

"""@router.get("/calendar")
async def calendar():
    return await get_calendar()"""


@router.post("/truncate-patients")
async def truncate_patients(
    token: Annotated[Token, Depends(require_staff_token)],
):
    await Account.filter(type=AccountType.PATIENT).delete()


@router.get("/{id}/to_parts")
async def interpret_pdf(
    id: int,
    token: Token = Depends(require_staff_token),
):
    document = await Document.get_or_none(id=id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if document.pdf is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return parts_to_raw(pdf_to_parts(document.pdf))


"""@router.post("/truncate-appointments")
async def truncate_appointments(
    token: Annotated[Token, Depends(require_staff_token)],
):
    await Appointment.all().delete()"""

"""
@router.get("/schedule")
async def make_initial_schedule(
    day_length: int,
    shift_offset: int,
    reserve_ratio: float,
):
    machines = []
    for resource in await Resource.all():
        machines.append(Machine(resource.id, resource.type))

    demands = []
    for demand in await Demand.all():
        cancer = get_cancer_type(demand.cancer_type)
        demands.append(DemandBind(
            demand.id, 
            demand.fractions,
            cancer.avg_duration,
            demand.fractions, 
            cancer.machine_options,
        ))

    print(2)
    result: list[AppointmentBind] = schedule(
        machines, 
        demands, 
        day_length, 
        reserve_ratio
    )
    print(3)

    appointments = []
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for appointment in result:

        start = now + datetime.timedelta(
            days=appointment.day, 
            minutes=appointment.start + shift_offset,
        )

        end = start + datetime.timedelta(minutes=appointment.duration)

        appointments.append(Appointment(
            demand_id=appointment.demand_id,
            resource_id=appointment.machine_id,
            start=start,
            end=end,
        ))
    
    await Appointment.all().delete()
    await Appointment.bulk_create(appointments)

    return [
        {
            "demand": appointment.demand_id,
            "resource": appointment.resource_id,
            "start": appointment.start,
            "end": appointment.end,
        }
        for appointment in appointments
    ]
"""
