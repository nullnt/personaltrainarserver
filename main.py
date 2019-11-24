from distutils.util import strtobool

from flask import Flask, request, jsonify
import datetime

from sklearn import svm

from setting import session
from userregistration import UserRegistration
import json

app = Flask(__name__)

# セッション変数の取得
from sqlalchemy import or_

# 種目マスタモデルの取得
from mitem import *
# 種目セットマスタモデルの取得
from mitemset import *
from setting import session
# トレーニング実施状況モデルの取得
from trainingstatus import *
# ユーザ登録情報モデルの取得
from userregistration import *


# チェックボックスのチェック有無設定
def checkBoxStatus(status):
    if status == 0:
        return False
    if status == 2:
        return True


# トレーニング実施状況の更新
def TrainingStatusUpdate(userid):
    trainingStatusquery = session.query(TrainingStatus)

    trainingStatus = trainingStatusquery.filter(UserRegistration.userid == userid). \
        filter(UserRegistration.endflag == "0"). \
        filter(UserRegistration.userid == TrainingStatus.userid). \
        filter(TrainingStatus.endflag == "0"). \
        first()

    return trainingStatus


# ユーザ情報登録の更新
def userRegistrationUpdate(userid):
    # ユーザ登録情報の更新
    userRegistrationquery = session.query(UserRegistration)

    userRegistration = userRegistrationquery.filter(UserRegistration.userid == userid). \
        filter(UserRegistration.endflag == "0"). \
        first()

    return userRegistration


# トレーニング実施画面の値設定
def tryView(userid, userInfoBase):
    users = session.query(UserRegistration, TrainingStatus, Mitem, Mitemset). \
        filter(UserRegistration.userid == userid). \
        filter(UserRegistration.endflag == "0"). \
        filter(UserRegistration.userid == TrainingStatus.userid). \
        filter(TrainingStatus.endflag == "0"). \
        filter(Mitemset.setno == TrainingStatus.setno). \
        filter(or_(Mitemset.traning1 == Mitem.traningseq, Mitemset.traning2 == Mitem.traningseq,
                   Mitemset.traning3 == Mitem.traningseq, )). \
        all()

    for user in users:
        if user.Mitem.traningseq == user.Mitemset.traning1:
            userInfoBase['mitem']['traning1']['mtraningname'] = user.Mitem.menuname
            userInfoBase['mitem']['traning1']['mtraningnum'] = str(user.Mitem.numberoftimes)
            userInfoBase['traningstuts']['traning1stuts'] = checkBoxStatus(user.TrainingStatus.traning1status)
        if user.Mitem.traningseq == user.Mitemset.traning2:
            userInfoBase['mitem']['traning2']['mtraningname'] = user.Mitem.menuname
            userInfoBase['mitem']['traning2']['mtraningnum'] = str(user.Mitem.numberoftimes)
            userInfoBase['traningstuts']['traning2stuts'] = checkBoxStatus(user.TrainingStatus.traning2status)
        if user.Mitem.traningseq == user.Mitemset.traning3:
            userInfoBase['mitem']['traning3']['mtraningname'] = user.Mitem.menuname
            userInfoBase['mitem']['traning3']['mtraningnum'] = str(user.Mitem.numberoftimes)
            userInfoBase['traningstuts']['traning3stuts'] = checkBoxStatus(user.TrainingStatus.traning3status)


# ユーザー登録情報の参照
def userRegistrationSelect(userid, userInfoBase):
    users = session.query(UserRegistration). \
        filter(UserRegistration.userid == userid). \
        filter(UserRegistration.endflag == "0"). \
        all()

    for user in users:
        # jsonユーザー情報.ユーザー情報.トレーニング実施完了フラグを設定
        userInfoBase['personaltrainar']['userid'] = user.userid
        # jsonユーザー情報.トレーニング実施完了フラグを設定
        userInfoBase['referenceResultFlag'] = True


@app.route('/implementationinput')
def implementationinput():

    if strtobool(request.args.get('training1')) and strtobool(request.args.get('training2')) and strtobool(request.args.get('training3')):
        # ユーザー登録情報の更新
        userRegistration = userRegistrationUpdate(request.args.get('userid'))

        # ユーザー情報.トレーニング実施完了フラグに"1:削除"を設定
        userRegistration.endflag = "1"

        # ユーザー情報.更新日時に現在日時を設定
        userRegistration.updatedate = datetime.datetime.now()

        # トレーニング実施状況の更新
        trainingStatus = TrainingStatusUpdate(request.args.get('userid'))

        # トレーニング実施状況.トレーニングnに"2:完了"を設定
        trainingStatus.traning1status = "2"
        trainingStatus.traning2status = "2"
        trainingStatus.traning3status = "2"

        # トレーニング実施状況.トレーニング実施完了フラグに"1:削除"を設定
        trainingStatus.endflag = "1"

        # トレーニング実施状況.更新日時に現在日時を設定
        trainingStatus.updatedate = datetime.datetime.now()

        session.commit()
        return "hello"

    else:
        # チェックボックス1がチェック有の場合
        if strtobool(request.args.get('training1')):
            # トレーニング実施状況の更新
            trainingStatus = TrainingStatusUpdate(request.args.get('userid'))
            # トレーニング実施状況.トレーニング1に"2:完了"を設定
            trainingStatus.traning1status = "2"
            # トレーニング実施状況.更新日時に現在日時を設定
            trainingStatus.updatedate = datetime.datetime.now()
            session.commit()
        else:
            # トレーニング実施状況の更新
            trainingStatus = TrainingStatusUpdate(request.args.get('userid'))
            # トレーニング実施状況.トレーニング1に"0:未着手"を設定
            trainingStatus.traning1status = "0"
            # トレーニング実施状況.更新日時に現在日時を設定
            trainingStatus.updatedate = datetime.datetime.now()
            session.commit()
        # チェックボックス2がチェック有の場合
        if strtobool(request.args.get('training2')):
            # トレーニング実施状況の更新
            trainingStatus = TrainingStatusUpdate(request.args.get('userid'))
            # トレーニング実施状況.トレーニング2に"2:完了"を設定
            trainingStatus.traning2status = "2"
            # トレーニング実施状況.更新日時に現在日時を設定
            trainingStatus.updatedate = datetime.datetime.now()
            session.commit()
        else:
            # トレーニング実施状況の更新
            trainingStatus = TrainingStatusUpdate(request.args.get('userid'))
            # トレーニング実施状況.トレーニング2に"0:未着手"を設定
            trainingStatus.traning2status = "0"
            # トレーニング実施状況.更新日時に現在日時を設定
            trainingStatus.updatedate = datetime.datetime.now()
            session.commit()
        # チェックボックス3がチェック有の場合
        if strtobool(request.args.get('training3')):
            # トレーニング実施状況の更新
            trainingStatus = TrainingStatusUpdate(request.args.get('userid'))
            # トレーニング実施状況.トレーニング3に"2:完了"を設定
            trainingStatus.traning3status = "2"
            # トレーニング実施状況.更新日時に現在日時を設定
            trainingStatus.updatedate = datetime.datetime.now()
            session.commit()
        else:
            # トレーニング実施状況の更新
            trainingStatus = TrainingStatusUpdate(request.args.get('userid'))
            # トレーニング実施状況.トレーニング3に"0:未着手"を設定
            trainingStatus.traning3status = "0"
            # トレーニング実施状況.更新日時に現在日時を設定
            trainingStatus.updatedate = datetime.datetime.now()
            session.commit()
        return "hello"


@app.route('/offercomplete')
def offercomplete():
    # 特徴量のデータ [1:脂肪を減らしたい2:筋肉を増やしたい, 1:お腹2:腹筋3:腹直筋,未知データ]
    feature = [
        [1, 1, 1],
        [1, 2, 5],
        [1, 3, 10],
        [2, 1, 3],
        [2, 2, 6],
        [2, 3, 8]
    ]
    # 正解のデータ 1:脂肪:弱, 2:脂肪:中, 3:脂肪:強, 4:筋肉:弱, 5:筋肉:中, 6:筋肉:強
    job = [1, 2, 3, 4, 5, 6]

    # 予測させるデータ 性別,部位,未知データ(トレーニング前後の体重差分)
    test_data = [
        [request.args.get('sex'), request.args.get('part'), request.args.get('weightdifference')]]

    # 学習
    clf = svm.SVC(gamma="scale")
    clf.fit(feature, job)

    # 学習結果を設定
    setno = clf.predict(test_data)[0]

    # ユーザ情報登録へINSERT
    session.add(UserRegistration(
        userid=request.args.get('userid'),
        sex=request.args.get('sex'),
        part=request.args.get('part'),
        age=request.args.get('age'),
        stature=request.args.get('stature'),
        beforeweight=request.args.get('beforeweight'),
        afterweight=request.args.get('afterweight'),
        trainingenddate=request.args.get('trainingenddate'),
        endflag="0",
        createdate=datetime.datetime.now(),
        updatedate=datetime.datetime.now()
    ))

    session.commit()

    # トレーニング実施状況へINSERT
    session.add(TrainingStatus(
        userid=request.args.get('userid'),
        setno=int(setno),
        traning1status=0,
        traning2status=0,
        traning3status=0,
        endflag="0",
        createdate=datetime.datetime.now(),
        updatedate=datetime.datetime.now()
    ))

    session.commit()

    # トレーニング実施画面の値設定
    tryView(userInfoBase['personaltrainar']['userid'], userInfoBase)
    return jsonify(userInfoBase)


@app.route('/logininput')
def logininput():
    with open('data/json/userinfo.json') as f:
        # jsonユーザー情報を共通情報として設定
        global userInfoBase
        userInfoBase = json.load(f)

        # jsonユーザー情報.トレーニング実施完了フラグを設定
        userInfoBase['referenceResultFlag'] = False

        # ユーザー登録情報の参照
        userRegistrationSelect(request.args.get('userid'), userInfoBase)

        # ユーザー登録情報のレコード情報有無の判定
        if userInfoBase['referenceResultFlag']:
            # トレーニング実施画面の値設定
            tryView(userInfoBase['personaltrainar']['userid'], userInfoBase)
        else:
            userInfoBase['personaltrainar']['userid'] = request.args.get('userid')
        return jsonify(userInfoBase)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
