from sqlalchemy.orm import Session

import models, schemas


def get_info_by_id(db: Session, id: int):
    return db.query(models.user).filter(models.user.id == id).first()


def get_info_by_dyid(db: Session, dyid: str):
    return db.query(models.user).filter(models.user.dyid == dyid).first()


def get_all_info(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user).offset(skip).limit(limit).all()



def create_info(db: Session, user: schemas.Createinfo):
    db_user = models.user(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_info_by_code(db: Session, user):
    db_user = models.user(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

'''
def change_data_by_code(db: Session, user):
    db_user = models.user(**user)
    mod_user = db.query(models.user).filter(models.user.dyid == db_user.dyid).first()
    mod_user.lottery_info = db_user.lottery_info
    db.commit()
    db.refresh(mod_user)
    return mod_user
'''


def delete_info_by_code(db: Session, dyid: str):
    mod_user = db.query(models.user).filter(models.user.dyid == dyid).first()
    db.delete(mod_user)
    db.commit()
    return mod_user