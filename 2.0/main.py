from fastapi import APIRouter, Depends, HTTPException, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from typing import List
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

@application.get("/")
async def temp(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


def input(db, i):
    try:
        db_user = curd.get_user_by_id(db, dyid=i["dyid"])  # 查询是否在库
        if (db_user != None):
            return "已入库，不再录入"
        else:
            curd.create_user_by_code(user=i, db=db)  # 不在库创建
            return i
    except:
        return "无效格式"
    

@application.post("/input/")
def input_data(
                    data: List,
                    background_tasks: BackgroundTasks,
                    db: Session = Depends(get_db)
                ):
    for i in data:
        background_tasks.add_task(input, db, i)
    return "信息已接收，后台检索入库中"





'''
@application.post("/create_user", response_model=schemas.Readuser, description="测试用，正常")
def create_user(user: schemas.Createuser, db: Session = Depends(get_db)): # json格式创建用户
    db_user = curd.get_user_by_id(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    return curd.create_user(db=db, user=user)
'''

@application.get("/get_data_by_dyid/{dyid}", response_model=schemas.Readuser)
def get_data_by_dyid(dyid: int, db: Session = Depends(get_db)):
    db_user = curd.get_user_by_id(db, dyid=dyid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


@application.get("/get_all_data/", response_model=List[schemas.Readuser])
def get_all_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)): # 查找所有用户数据
    users = curd.get_users(db, skip=skip, limit=limit)
    return users


@application.get("/delete_data_by_dyid/{dyid}")
def delete_data(dyid: int, db: Session = Depends(get_db)): # 指定用户数据删除
    delete_user = curd.delete_user_by_code(db, dyid=dyid)
    return delete_user

def check_real_datas(db,s):
    while True:
        temp_url = url_ip + 'sync/get_users/' + admin + '/'
        r = requests.get(temp_url)
        for i in r.json():
            t = datetime.datetime.strptime(i["updated_at"][0:10]+" "+i["updated_at"][11:], "%Y-%m-%d %H:%M:%S")
            if t+datetime.timedelta(days=s) < datetime.datetime.utcnow():
                curd.delete_user_by_code(db, i["id"])
        time.sleep(300)


temp = 0

@application.get("/sync/",description="开始循环检测并删除过期记录,s为入库后自动删除的时间(天),部署后该接口必须请求一次")
def check_data_by_time(s: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)): # 指定用户数据删除
    global temp
    if temp == 0:
        background_tasks.add_task(check_real_datas, db, s)
        temp = s
        return "循环检索，删除入库超过{}天的数据".format(s)
    else:
        return "已经设定删除入库超过{}天的数据，请勿重复操作，".format(temp)
