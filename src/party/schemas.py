from datetime import datetime

from pydantic import BaseModel


class PartyCreate(BaseModel):
    title: str
    description: str
    date: datetime
    owner_id: int
