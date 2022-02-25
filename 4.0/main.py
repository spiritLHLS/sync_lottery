from fastapi import APIRouter, Depends, HTTPException, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from typing import List, Set
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime, time
import schemas, curd
from database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)


application = APIRouter()


templates = Jinja2Templates(directory='./templates')
Session = requests.session()
scheduler = BackgroundScheduler()
scheduler.start()

#一些重要自定义参数
admin="spiritlhl"
url_ip="http://127.0.0.1:3333/"

requests.packages.urllib3.disable_warnings()


def get_db(): # 数据库依赖
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
@application.get("/")
async def temp(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
'''

def input(db, i):
    db_user = curd.get_info_by_dyid(db, dyid=i["dyid"])  # 查询是否在库
    if (db_user != None):
        return "已入库，不再录入"
    else:
        try:
            i["uid"]
        except:
            i["uid"] = []
        else:
            pass

        try:
            i["isOfficialLottery"]
        except:
            i["isOfficialLottery"] = ""

        try:
            i["relay_chat"]
        except:
            i["relay_chat"] = ""

        try:
            i["ctrl"]
        except:
            i["ctrl"] = ""

        try:
            i["rid"]
        except:
            i["rid"] = ""

        try:
            i["chat_type"]
        except:
            i["chat_type"] = 0
        curd.create_info_by_code(user=i, db=db)  # 不在库创建
        return i

@application.post("/set_lottery_info/")
def input_data(
                    lottery_info: List,
                    background_tasks: BackgroundTasks,
                    db: Session = Depends(get_db)
                ):
    for i in lottery_info:
        background_tasks.add_task(input, db, i)
    return "OK"

@application.get("/get_info_by_dyid/{dyid}", response_model=schemas.ReadData)
def get_info_by_dyid(dyid: str, db: Session = Depends(get_db)):
    db_user = curd.get_info_by_dyid(db, dyid=dyid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


@application.get("/get_lottery_info/")
def get_all_info(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)): # 查找所有用户数据
    datas = curd.get_all_info(db, skip=skip, limit=limit)
    if datas != None:
        return {
            "err_msg": "",
            "lottery_info": datas
        }
    else:
        return {
            "err_msg": "error",
            "lottery_info": ""
        }


@application.get("/delete_info_by_dyid/{dyid}")
def delete_info_by_dyid(dyid: str, db: Session = Depends(get_db)): # 指定用户数据删除
    delete_user = curd.delete_info_by_code(db, dyid=dyid)
    return delete_user

def check_real_info(db,s):
    while True:
        temp_url = url_ip + 'sync/get_users/' + admin + '/'
        r = requests.get(temp_url)
        for i in r.json():
            t = datetime.datetime.strptime(i["updated_at"][0:10]+" "+i["updated_at"][11:], "%Y-%m-%d %H:%M:%S")
            if t+datetime.timedelta(days=s) < datetime.datetime.utcnow():
                curd.delete_info_by_code(db, i["id"])
        time.sleep(300)


temp = 0

@application.get("/sync/",description="开始循环检测并删除过期记录,s为入库后自动删除的时间(天),部署后该接口必须请求一次")
def check_data_by_time(s: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)): # 指定用户数据删除
    global temp
    if temp == 0:
        background_tasks.add_task(check_real_info, db, s)
        temp = s
        return "循环检索，删除入库超过{}天的数据".format(s)
    else:
        return "已经设定删除入库超过{}天的数据，请勿重复操作，".format(temp)
