import sys

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from setting import Base
from setting import ENGINE


class Mitemset(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'mitemset'
    setno = Column(Integer, primary_key=True)
    traning1 = Column(Integer)
    traning2 = Column(Integer)
    traning3 = Column(Integer)
    createdate = Column(DateTime)
    updatedate = Column(DateTime)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)