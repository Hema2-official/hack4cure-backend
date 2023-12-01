from fastapi import APIRouter, HTTPException, status, Depends, Response, UploadFile, File

from models import *

from typing import Annotated, Optional

from dependencies.auth import require_account, require_staff_token, Token


router = APIRouter(tags=["forms"])


@router.get("")
async def get_forms(
    token: Token = Depends(require_staff_token),
):
    forms = await Form.all()
    return [
        await FormResponse.create(form) 
        for form in forms
    ]


@router.get("/{id}")
async def get_form(
    id: int,
    token: Token = Depends(require_staff_token),
):
    form = await Form.get_or_none(id=id)
    if form is None:
        raise HTTPException(status_code=404)
    return await FormResponse.create(form)


class FormBody(BaseModel):
    name: str
    fields: list[FormField]


@router.post("")
async def create_form(
    body: FormBody,
    token: Token = Depends(require_staff_token),
):
    form = await Form.create(
        name=body.name,
        fields=[field.dict() for field in body.fields],
    )
    return await FormResponse.create(form)


@router.delete("/{id}")
async def delete_form(
    id: int,
    token: Token = Depends(require_staff_token),
):
    await Form.filter(id=id).delete()
