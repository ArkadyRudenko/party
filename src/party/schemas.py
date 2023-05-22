from datetime import datetime, date

from pydantic import BaseModel


class PartyCreate(BaseModel):
    title: str
    description: str
    date: datetime


class PartyRead(BaseModel):
    id: int
    title: str
    description: str
    created_at: date
    date: date
    owner_id: int
    count_of_guests: int
