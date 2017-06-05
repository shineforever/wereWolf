#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class UserInfo(db.Model):
    __tablename__ = 'UserInfo'
    userID = db.Column(db.String(100), primary_key=True)
    userName = db.Column(db.String(100))
    openID = db.Column(db.String(100))
    gender = db.Column(db.Integer)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    userType = db.Column(db.Integer)
    createTime = db.Column(db.DateTime)

    club = db.relationship('Club', backref='UserInfo', lazy='dynamic')
    judge = db.relationship('Judge', backref='UserInfo', lazy='dynamic')
    participate = db.relationship('Participate', backref='UserInfo', lazy='dynamic')

    def __init__(self, userID=None, openID=None, userName=None,
                 gender=0, longitude=118.46, latitude=32.03,
                 userType=1, createTime=None):
        self.userID = userID
        self.openID = openID
        self.userName = userName
        self.gender = gender
        self.longitude = longitude
        self.latitude = latitude
        self.userType = userType
        self.createTime = createTime




    def __repr__(self):
        return self.userID


    @staticmethod
    def create(info):
        userID = info['userID']
        userName = info['userName']
        gender = info['gender']
        longitude = info['longitude']
        latitude = info['latitude']
        userType = info['userType']
        createTime = info['createTime']
        openID = info['openID']
        userInfo = UserInfo(
            userID=userID, userName=userName, gender=gender,
            longitude=longitude, latitude=latitude, userType=userType,
            createTime=createTime, openID=openID
        )
        db.session.add(userInfo)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['userID'] = result.userID
        res['userName'] = result.userName
        res['gender'] = result.gender
        res['longitude'] = result.longitude
        res['latitude'] = result.latitude
        res['userType'] = result.userType
        res['createTime'] = str(result.createTime)
        res['userType'] = result.userType
        return (True, res)
