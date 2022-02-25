from datetime import date as date_
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class CreateData(BaseModel):
    date: date_

class Createinfo(BaseModel):
    uid: Optional[List[int]]
    dyid: str
    isOfficialLottery: Optional[str]
    relay_chat: Optional[str]
    ctrl: Optional[str]
    rid: Optional[str]
    chat_type: Optional[int]

class ReadData(BaseModel):
    uid: Optional[List[int]]
    dyid: str
    isOfficialLottery: Optional[str]
    relay_chat: Optional[str]
    ctrl: Optional[str]
    rid: Optional[str]
    chat_type: Optional[int]

    class Config:
        orm_mode = True


class Readinfo(ReadData):
    err_msg: str
    lottery_info: Optional[ReadData]

    class Config:
        orm_mode =  True