#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Participate(db.Model):
    __tablename__ = 'Participate'
    participateID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    activityID = db.Column(db.String(100), db.ForeignKey('Activity.activityID'))
    createTime = db.Column(db.DateTime)

    def __init__(self, participateID=None, userID=None, activityID=None,
                 createTime=None):
        self.participateID = participateID
        self.userID = userID
        self.activityID = activityID
        self.createTime = createTime




    def __repr__(self):
        return self.participateID


    @staticmethod
    def create(info):
        participateID = info['participateID']
        userID = info['userID']
        activityID = info['activityID']
        createTime = info['createTime']
        participate = Participate(
            participateID=participateID, userID=userID, activityID=activityID,
            createTime=createTime
        )
        db.session.add(participate)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['participateID'] = result.participateID
        res['userID'] = result.userID
        res['activityID'] = result.activityID
        res['createTime'] = str(result.createTime)
        return (True, res)
