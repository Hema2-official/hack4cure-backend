from fastapi import APIRouter, HTTPException, status, Depends, Response, UploadFile, File

from models import *

from typing import Annotated, Optional

from dependencies.auth import require_account, require_staff_token, Token

import common.calendar

router = APIRouter(tags=["documents"])


@router.get("")
async def get_documents(
    token: Token = Depends(require_staff_token),
    patient_id: Optional[int] = None,
):
    if patient_id is None:
        pdfs = await PDF.all()
        form_submissions = await FormSubmission.all()
    else:
        pdfs = await PDF.filter(patient_id=patient_id)
        form_submissions = await FormSubmission.filter(patient_id=patient_id)

    documents = pdfs + form_submissions

    return [
        await DocumentResponse.create(document, include_data=False)
        for document in documents
    ]


@router.get("/calendar")
async def get_calendar(
    token: Token = Depends(require_staff_token),
):
    return await common.calendar.get_calendar()


class PDFBody(BaseModel):
    patient_id: int
    form_id: int
    timestamp: datetime.datetime


@router.post("/pdf")
async def upload_pdf (
    body: PDFBody,
    file: UploadFile = File(...),
    token: Token = Depends(require_staff_token),
):
    pdf = await PDF.create(
        patient_id=body.patient_id,
        form_id=body.form_id,
        timestamp=body.timestamp,
        file=await file.read(),
    )

    await pdf.save()


class FormSubmissionBody(BaseModel):
    patient_id: int
    form_id: int
    timestamp: Optional[datetime.datetime]
    data: dict


@router.post("/form")
async def upload_form (
    body: FormSubmissionBody,
    token: Token = Depends(require_staff_token),
):
    form_submission = await FormSubmission.create(
        patient_id=body.patient_id,
        form_id=body.form_id,
        timestamp=body.timestamp,
        data=body.data,
    )

    await form_submission.save()


@router.delete("/{id}")
async def delete_document(
    id: int,
    token: Token = Depends(require_staff_token),
):
    await Document.filter(id=id).delete()


@router.get("/{id}")
async def get_document(
    id: int,
    token: Token = Depends(require_staff_token),
):
    pdf = await PDF.get_or_none(id=id)
    if pdf is not None:
        return await DocumentResponse.create(pdf, include_data=True)
    
    form_submission = await FormSubmission.get_or_none(id=id)
    if form_submission is not None:
        return await DocumentResponse.create(form_submission, include_data=True)
    