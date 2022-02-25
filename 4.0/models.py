from sqlalchemy import Column, String, Integer, DateTime, func, BigInteger, PickleType
from database import Base


class user(Base):
    __tablename__ = 'data'  # 数据表的表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(PickleType, unique=False, nullable=False, comment='lottery_info')
    dyid = Column(String(1000), unique=False, nullable=False, comment='dyid')
    isOfficialLottery = Column(PickleType, unique=False, nullable=False, comment='lottery_info')
    relay_chat = Column(PickleType, unique=False, nullable=False, comment='lottery_info')
    ctrl = Column(String(1000), unique=False, nullable=False, comment='lottery_info')
    rid = Column(String(1000), unique=False, nullable=False, comment='lottery_info')
    chat_type = Column(Integer, unique=False, nullable=False, comment='lottery_info')


    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {"order_by": created_at.desc()}  # 默认是正序，倒序加上.desc()方法

    def __repr__(self):
        return f'{self.uid}_{self.dyid}_{self.isOfficialLottery}_{self.relay_chat}_{self.ctrl}_{self.rid}_{self.chat_type}'