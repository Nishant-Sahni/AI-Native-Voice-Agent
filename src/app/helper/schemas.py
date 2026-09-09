from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class HotelOut(BaseModel):
    id: UUID
    name: str
    phone: Optional[str]

    class Config:
        orm_mode = True
