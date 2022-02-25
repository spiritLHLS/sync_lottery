from datetime import date as date_
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class CreateData(BaseModel):
    date: date_

class Createinfo(BaseModel):
    uid: List[int]
    dyid: str
    isOfficialLottery: bool
    relay_chat: str
    ctrl: str
    rid: str
    chat_type: int

class ReadData(Createinfo):
    id: int
    uid: List[int]
    dyid: str
    isOfficialLottery: bool
    relay_chat: str
    ctrl: str
    rid: str
    chat_type: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class Readinfo(Createinfo):
    uid: List[int]
    dyid: str
    isOfficialLottery: bool
    relay_chat: str
    ctrl: str
    rid: str
    chat_type: int

    class Config:
        orm_mode =  True