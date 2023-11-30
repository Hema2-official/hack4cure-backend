from tortoise import fields, models
from fastapi import HTTPException, status

from enum import Enum, StrEnum
import time
import datetime
from typing import Optional

from pydantic import BaseModel

from common.cancer_types import CancerType, get_cancer_type


class AccountType(StrEnum):
    PATIENT = "patient"
    STAFF = "staff"


class Account(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=254, unique=True, null=True)

    password = fields.TextField(null=True)
    google_id = fields.TextField(null=True)

    first_name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)

    created_at = fields.IntField() # unix timestamp
    updated_at = fields.IntField() # unix timestamp

    type = fields.CharEnumField(AccountType, default=AccountType.STAFF)

    async def update(self):
        self.updated_at = int(time.time())
        return await self.save()


class AccountResponse(BaseModel):
    id: int
    email: Optional[str]
    google_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: int
    updated_at: int
    type: AccountType

    @classmethod
    async def create(cls, account: Account):
        return cls(
            id=account.id,
            email=account.email,
            google_id=account.google_id,
            first_name=account.first_name,
            last_name=account.last_name,
            created_at=account.created_at,
            updated_at=account.updated_at,
            type=account.type,
        )


class Log(models.Model):
    id = fields.IntField(pk=True)
    timestamp = fields.DatetimeField(auto_now_add=True)
    text = fields.TextField() # The log itself


class LogResponse(BaseModel):
    id: int
    timestamp: datetime.datetime
    text: str

    @classmethod
    async def create(cls, log: Log):
        return cls(
            id=log.id,
            timestamp=log.timestamp,
            text=log.text,
        )


class Form(models.Model):
    id = fields.IntField(pk=True)
    fields = fields.JSONField()


class FormResponse(BaseModel):
    id: int
    fields: dict

    @classmethod
    async def create(cls, form: Form):
        return cls(
            id=form.id,
            fields=form.fields,
        )
    

class Document(models.Model):
    id = fields.IntField(pk=True)
    account = fields.ForeignKeyField("models.Account")
    form = fields.ForeignKeyField("models.Form")
    timestamp = fields.DatetimeField(auto_now_add=True)

    def get_data(self) -> dict:
        return {}


class DocumentResponse(BaseModel):
    id: int
    account: AccountResponse
    form: FormResponse
    timestamp: datetime.datetime
    data: dict

    @classmethod
    async def create(cls, document: Document, data: dict = {}):
        return cls(
            id=document.id,
            account=await AccountResponse.create(document.account),
            form=await FormResponse.create(document.form),
            timestamp=document.timestamp,
            data=data,
        )
    

class PDF(Document):
    file = fields.BinaryField()


class FormSubmission(Document):
    data = fields.JSONField()

    def get_data(self) -> dict:
        return self.data
