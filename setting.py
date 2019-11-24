from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

# mysqlのDBの設定
# 接続ホスト名: localhost
# データベース名: db_personaltrainar
# ユーザー名: root
# パスワード: root
# 文字コード: UTF-8
# SQLログを表示したい場合には echo=True を指定
DATABASE = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
    "root",  # user_name
    "root",  # password
    "localhost",  # host_ip
    "db_personaltrainar"  # db_name
)
ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True  # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
session = scoped_session(
  # ORM実行時の設定。自動コミットするか、自動反映するなど。
     sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
     )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()
