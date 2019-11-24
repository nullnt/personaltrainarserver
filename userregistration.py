import logging
import sys

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from setting import Base
from setting import ENGINE


class UserRegistration(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'userregistration'
    userid = Column(String(32), primary_key=True)
    sex = Column(String(1))
    part = Column(String(1))
    age = Column(Integer)
    stature = Column(Integer)
    beforeweight = Column(Integer)
    afterweight = Column(Integer)
    trainingenddate = Column(DateTime)
    endflag = Column(String(1), primary_key=True)
    createdate = Column(DateTime)
    updatedate = Column(DateTime)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)
