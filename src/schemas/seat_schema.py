from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class SeatCreate(BaseModel):
    num: int
    stadium_id: int


class SeatRead(BaseModel):
    id: int
    num: int
    stadium: Optional["StadiumForSeat"] = None
    model_config = ConfigDict(from_attributes=True)


class SeatForStadium(BaseModel):
    id: int
