import sys

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from setting import Base
from setting import ENGINE


class Mitem(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'mitem'
    traningseq = Column(Integer, primary_key=True)
    importance = Column(Integer)
    menuname = Column(String(32))
    numberoftimes = Column(Integer)
    createdate = Column(DateTime)
    updatedate = Column(DateTime)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)