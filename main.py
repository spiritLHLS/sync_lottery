from fastapi import APIRouter, Depends, HTTPException, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from typing import List, Set
from apscheduler.schedulers.background import BackgroundScheduler
import requests, json
import datetime, time, random
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
    try:
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()
    except:
        print("error")

def input(db, lottery_info):
    for i in lottery_info:
        db_user = curd.get_info_by_dyid(db, dyid=i["dyid"])  # 查询是否在库
        if (db_user != None):
            print("已入库，不再录入")
        else:
            try:
                i["lottery_info_type"]
            except:
                i["lottery_info_type"] = ""
    
            try:
                i["create_time"]
            except:
                i["create_time"] = 0
    
            try:
                i["is_liked"]
            except:
                i["is_liked"] = ""
    
            try:
                i["uids"]
            except:
                i["uids"] = []
    
            try:
                i["uname"]
            except:
                i["uname"] = ""
    
            try:
                i["ctrl"]
            except:
                i["ctrl"] = ""
    
            try:
                i["rid"]
            except:
                i["rid"] = ""
    
            try:
                i["des"]
            except:
                i["des"] = ""
    
            try:
                i["type"]
            except:
                i["type"] = ""
    
            try:
                i["hasOfficialLottery"]
            except:
                i["hasOfficialLottery"] = ""
            
            status_f = 0
            if i["uids"] != []:
                for j in i['uids']:
                    if j != None and status_f == 0:
                        try:
                            tp = requests.get("https://tenapi.cn/bilibilifo/?uid="+str(j)).json()
                            time.sleep(random.uniform(1.1,3.1))
                            num = tp["data"]["follower"]
                            if num >= 10000:
                                status_f = 1
                            else:
                                try:
                                    tp = requests.get("https://api.bilibili.com/x/relation/stat?vmid="+str(j)+"&jsonp=jsonp").json()
                                    time.sleep(random.uniform(1.1,3.1))
                                    num2 = tp["data"]["follower"]
                                    if num2 >= 10000:
                                        status_f = 1
                                    else:
                                        status_f = 2
                                except:
                                    status_f = 2
                        except:
                            try:
                                tp = requests.get("https://api.bilibili.com/x/relation/stat?vmid="+str(j)+"&jsonp=jsonp").json()
                                time.sleep(random.uniform(1.1,3.1))
                                num2 = tp["data"]["follower"]
                                if num2 >= 10000:
                                    status_f = 1
                                else:
                                    status_f = 2
                            except:
                                status_f = 2
                    elif status_f == 1:
                        curd.create_info_by_code(user=i, db=db)  # 不在库创建
                        status_f = 2
                    elif status_f == 2:
                        status_f = 0
                        continue
                if status_f == 1:
                    curd.create_info_by_code(user=i, db=db)  # 不在库创建
                    status_f = 2
            else:
                curd.create_info_by_code(user=i, db=db)  # 不在库创建


@application.post("/set_lottery_info/")
def input_data(
                    lottery_info: List,
                    background_tasks: BackgroundTasks,
                    db: Session = Depends(get_db)
                ):
    background_tasks.add_task(input, db, lottery_info)
    return "OK"

@application.get("/get_info_by_dyid/{dyid}")
def get_info_by_dyid(dyid: str, db: Session = Depends(get_db)):
    db_user = curd.get_info_by_dyid(db, dyid=dyid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


@application.get("/get_lottery_info/")
def get_all_info(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)): # 查找所有用户数据
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


@application.get("/get_lottery_Officialinfo/")
def get_all_Officialinfo(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)): # 查找所有用户数据
    datas = curd.get_all_info_OfficialLottery(db, skip=skip, limit=limit)
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

@application.get("/get_lottery_isnotOfficialinfo/")
def get_all_isnotOfficialinfo(skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)): # 查找所有用户数据
    datas = curd.get_all_info_isnotOfficialLottery(db, skip=skip, limit=limit)
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
    db_user = curd.get_info_by_dyid(db, dyid=dyid)
    if (db_user != None):
        curd.delete_info_by_code(db, dyid=dyid)
        return "OK"
    else:
        return "不存在数据"

def check_only(db,r):
    tpdyid = []
    for i in r:
        if str(i).split("&")[2] not in tpdyid:
            tpdyid.append(str(i).split("&")[2])
        else:
            curd.delete_id_by_code(db, str(i).split("&")[0])


def check_real_info(db,s):
    r = curd.get_all_info(db)
    #check_only(db, r.json()['lottery_info'])
    for i in r:
        t = datetime.datetime.strptime(str(i).split("&")[-1][0:10]+" "+str(i).split("&")[-1][11:], "%Y-%m-%d %H:%M:%S")
        if t+datetime.timedelta(days=s) < datetime.datetime.utcnow():
            curd.delete_id_by_code(db, str(i).split("&")[0])
        #requests.get(url_ip+"lottery/save_json/")

def check_real(db,s,r):
    for i in r:
        t = datetime.datetime.strptime(str(i).split("&")[-1][0:10]+" "+str(i).split("&")[-1][11:], "%Y-%m-%d %H:%M:%S")
        if t+datetime.timedelta(days=s) < datetime.datetime.utcnow():
            curd.delete_id_by_code(db, str(i).split("&")[0])

def save(datas):
    with open("./archive_datas/datas.json", 'w', encoding='utf-8') as json_file:
        json.dump(datas, json_file, ensure_ascii=False)
    return "OK"

def archive(datas):
    with open("./archive_datas_by_days/{}.json".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')[0:10] + "_" + datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')[11:]), 'w', encoding='utf-8') as json_file_d:
        json.dump(datas, json_file_d, ensure_ascii=False)
    return "OK"

def save_50(datas):
    with open("./archive_datas/50datas.json", 'w', encoding='utf-8') as json_file:
        json.dump(datas, json_file, ensure_ascii=False)
    return "OK"

@application.get("/save_json/", description="保存数据为json文件")
def save_json():
    datas1 = requests.get(url_ip+"lottery/get_lottery_info/?skip=0&limit=150")
    datas2 = requests.get(url_ip+"lottery/get_lottery_info/?skip=0&limit=20000")
    datas3 = requests.get(url_ip+"lottery/get_lottery_info/?skip=0&limit=50")
    scheduler.add_job(func=save, args=(datas1.json()), next_run_time=datetime.datetime.now())
    scheduler.add_job(func=archive, args=(datas2.json()), next_run_time=datetime.datetime.now())
    scheduler.add_job(func=save_50, args=(datas3.json()), next_run_time=datetime.datetime.now())
    return "OK"

@application.get("/check/",description="检查一次入库数据")
def check_data(s: int, db: Session = Depends(get_db)):
    r = curd.get_all_info(db)
    scheduler.add_job(func=check_real, args=(db, s, r), next_run_time=datetime.datetime.now())
    scheduler.add_job(func=check_only, args=(db, r), next_run_time=datetime.datetime.now())
    return "循环检索，删除入库超过{}天的数据，目前库内数据共{}条".format(s, len(r))
    

temp = 0


@application.get("/sync/",description="开始循环检测并删除过期记录,s为入库后自动删除的时间(天),部署后该接口必须请求一次")
def check_data_by_time(s: int, db: Session = Depends(get_db)): # 指定用户数据删除
    global temp
    if temp == 0:
        scheduler.add_job(func=check_real_info, args=(db, s), trigger='interval', seconds=60*60*12)
        temp = s
        return "循环检索，删除入库超过{}天的数据".format(s)
    else:
        return "已经设定删除入库超过{}天的数据，请勿重复操作，".format(temp)
