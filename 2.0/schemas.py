from datetime import date as date_
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class CreateData(BaseModel):
    date: date_

class Createuser(BaseModel):
    dyid: int
    lottery_info: str

class ReadData(CreateData):
    dyid: int
    lottery_info: str
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class Readuser(Createuser):
    dyid: int
    lottery_info: str
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode =  True