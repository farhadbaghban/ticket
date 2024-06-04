from pydantic import BaseModel, ConfigDict
from typing import List
from .seat_schema import SeatForStadium


class StadiumCreate(BaseModel):
    name: str
    seat_num: int


class StadiumRead(BaseModel):
    id: int
    name: str
    seat_num: int
    seats: List[SeatForStadium] = []

    model_config = ConfigDict(from_attributes=True)


class StadiumForSeat(BaseModel):
    name: str
