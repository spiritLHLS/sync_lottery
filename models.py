from sqlalchemy import Column, String, Integer, DateTime, func, BigInteger, PickleType
from database import Base


class user(Base):
    __tablename__ = 'data'  # 数据表的表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lottery_info_type = Column(String(1000), unique=False, nullable=False, comment='lottery_info_type')
    create_time = Column(Integer, unique=False, nullable=False, comment='create_time')
    is_liked = Column(PickleType, unique=False, nullable=False, comment='is_liked')
    uids = Column(PickleType, unique=False, nullable=False, comment='uids')
    uname = Column(PickleType, unique=False, nullable=False, comment='uname')
    ctrl = Column(PickleType, unique=False, nullable=False, comment='ctrl')
    dyid = Column(PickleType, unique=False, nullable=False, comment='dyid')
    rid = Column(String(1000), unique=False, nullable=False, comment='rid')
    des = Column(PickleType, unique=False, nullable=False, comment='des')
    type = Column(Integer, unique=False, nullable=False, comment='type')
    hasOfficialLottery = Column(PickleType, unique=False, nullable=False, comment='hasOfficialLottery')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {"order_by": created_at.desc()}  # 默认是正序，倒序加上.desc()方法

    def __repr__(self):
        return f'{self.id}&{self.create_time}&{self.dyid}&{self.updated_at}'
