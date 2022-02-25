from sqlalchemy.orm import Session
import models, schemas


def get_info_by_id(db: Session, id: int):
    return db.query(models.user).filter(models.user.id == id).first()


def get_info_by_dyid(db: Session, dyid: str):
    return db.query(models.user).filter(models.user.dyid == dyid).first()


def get_all_info(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user).offset(skip).limit(limit).all()


def create_info(db: Session, user: schemas.Createuser):
    db_user = models.user(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

