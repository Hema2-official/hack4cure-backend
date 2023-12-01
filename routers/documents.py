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
        documents = await Document.all()
    else:
        documents = await Document.filter(patient_id=patient_id)

    return [
        await DocumentResponse.create(document, include_data=True)
        for document in documents
    ]


@router.get("/calendar")
async def get_calendar(
    token: Token = Depends(require_staff_token),
):
    return await common.calendar.get_calendar()


class FormSubmissionBody(BaseModel):
    patient_id: int
    form_id: int
    timestamp: Optional[datetime.datetime]
    data: Optional[dict]


@router.post("/form")
async def upload_form (
    body: FormSubmissionBody,
    token: Token = Depends(require_staff_token),
):
    document = await Document.create(
        patient_id=body.patient_id,
        form_id=body.form_id,
        timestamp=body.timestamp,
        data=body.data,
    )

    if body.data is not None and not await document.validate():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data format does not match the form.",
        )

    await document.save()
    return await DocumentResponse.create(document, include_data=True)


class FormSubmissionPatchBody(BaseModel):
    timestamp: Optional[datetime.datetime]
    data: Optional[dict]


@router.patch("/{id}")
async def patch_form(
    id: int,
    body: FormSubmissionPatchBody,
    token: Token = Depends(require_staff_token),
):
    document = await Document.get_or_none(id=id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    document.update_from_dict(body.dict(exclude_unset=True))

    if body.data is not None and not await document.validate():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data format does not match the form.",
        )

    await document.save()


@router.post("/{id}/pdf")
async def upload_pdf(
    id: int,
    file: UploadFile = File(...),
    token: Token = Depends(require_staff_token),
):
    await Document.filter(id=id).update(pdf=file.file.read())


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
    document = await Document.get_or_none(id=id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await DocumentResponse.create(document, include_data=True)


@router.get("/{id}/pdf", response_class=Response)
async def get_document_pdf(
    id: int,
    token: Token = Depends(require_staff_token),
):
    document = await Document.get_or_none(id=id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if document.pdf is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(
        content=document.pdf, 
        media_type="application/octet-stream", 
        headers={"Content-Disposition": f"attachment; filename=document-{document.id}.pdf"}
    )


@router.get("/autocomplete")
async def autocomplete_documents(
    patient_id: int,
    form_id: int,
    token: Token = Depends(require_staff_token),
):
    return {}
