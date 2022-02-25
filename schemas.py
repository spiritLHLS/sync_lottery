from datetime import date as date_
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class CreateData(BaseModel):
    date: date_

class Createinfo(BaseModel):
    lottery_info_type: Optional[str]
    create_time: Optional[int]
    is_liked: Optional[str]
    uids: Optional[List[int]]
    uname: Optional[str]
    ctrl: Optional[str]
    dyid: str
    rid: Optional[str]
    des: Optional[str]
    type: Optional[int]
    hasOfficialLottery: Optional[str]

class ReadData(BaseModel):
    lottery_info_type: Optional[str]
    create_time: Optional[int]
    is_liked: Optional[str]
    uids: Optional[List[int]]
    uname: Optional[str]
    ctrl: Optional[str]
    dyid: str
    rid: Optional[str]
    des: str
    type: Optional[int]
    hasOfficialLottery: Optional[str]

    class Config:
        orm_mode = True


class Readinfo(ReadData):
    err_msg: str
    lottery_info: Optional[ReadData]

    class Config:
        orm_mode =  True