from tortoise import fields, models
from fastapi import HTTPException, status

from enum import Enum, StrEnum
import time
import datetime
from typing import Optional

from pydantic import BaseModel


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


class FormFieldType(StrEnum):
    TEXT = "text"
    NUMBER = "number"
    DATETIME = "datetime"


class FormField(BaseModel):
    name: str
    description: str
    type: FormFieldType


class Form(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    fields = fields.JSONField()


class FormResponse(BaseModel):
    id: int
    name: str
    fields: list[FormField]

    @classmethod
    async def create(cls, form: Form):
        return cls(
            id=form.id,
            name=form.name,
            fields=form.fields,
        )
    

class Document(models.Model):
    id = fields.IntField(pk=True)
    patient = fields.ForeignKeyField("models.Account")
    form = fields.ForeignKeyField("models.Form")
    timestamp = fields.DatetimeField(auto_now_add=True)
    pdf = fields.BinaryField(null=True)
    data = fields.JSONField(null=True)

    def get_data(self) -> dict:
        if self.data is None:
            return {}
        return self.data
    
    async def validate(self) -> bool:
        for field in (await self.form).fields:
            if field["name"] not in self.data:
                return False
            
            if field["type"] == FormFieldType.NUMBER:
                try:
                    float(self.data[field.name])
                except ValueError:
                    return False
                
            if field["type"] == FormFieldType.DATETIME:
                try:
                    datetime.datetime.fromisoformat(self.data[field.name])
                except ValueError:
                    return False
                
            if field["type"] == FormFieldType.TEXT:
                if not isinstance(self.data[field["name"]], str):
                    return False

        return True


class DocumentResponse(BaseModel):
    id: int
    patient_id: int
    form_id: int
    timestamp: datetime.datetime
    data: Optional[dict]

    @classmethod
    async def create(cls, document: Document, include_data: bool = False):
        if include_data:
            data = document.get_data()
        else:
            data = None

        return cls(
            id=document.id,
            patient_id=document.patient_id,
            form_id=document.form_id,
            timestamp=document.timestamp,
            data=data,
        )
