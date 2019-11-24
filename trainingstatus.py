import sys

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from setting import Base
from setting import ENGINE


class TrainingStatus(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'trainingstatus'
    userid = Column(String(32), primary_key=True)
    setno = Column(Integer)
    traning1status = Column(Integer)
    traning2status = Column(Integer)
    traning3status = Column(Integer)
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
