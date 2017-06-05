#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Activity(db.Model):
    __tablename__ = 'Activity'
    activityID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    activityName = db.Column(db.String(100))
    fee = db.Column(db.String(100))
    entryStartDate = db.Column(db.DateTime)
    entryEndDate = db.Column(db.DateTime)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    minNumber = db.Column(db.Integer)
    maxNumber = db.Column(db.Integer)
    typeID = db.Column(db.Integer)
    clubID = db.Column(db.String(100), db.ForeignKey('Club.clubID'))
    description = db.Column(db.Text)
    area =db.Column(db.Text)
    createTime = db.Column(db.DateTime)
    participateState = db.Column(db.Boolean)

    participate = db.relationship('Participate', backref='Activity', lazy='dynamic')

    def __init__(self, activityID=None, userID=None, entryStartDate=None,
                 entryEndDate=None, startDate=None, endDate=None,
                 activityName=None, minNumber=1, maxNumber=None,
                 typeID=None, clubID=None, description=None,
                 area=None, createTime=None, fee=None, participateState=True):
        self.activityID = activityID
        self.userID = userID
        self.entryStartDate = entryStartDate
        self.entryEndDate = entryEndDate
        self.startDate = startDate
        self.endDate = endDate
        self.activityName = activityName
        self.minNumber = minNumber
        self.maxNumber = maxNumber
        self.typeID = typeID
        self.clubID = clubID
        self.description = description
        self.area = area
        self.createTime = createTime
        self.fee = fee
        self.participateState = participateState

    def __repr__(self):
        return self.activityID


    @staticmethod
    def create(info):
        activityID = info['activityID']
        activityName = info['activityName']
        userID = info['userID']
        entryStartDate = info['entryStartDate']
        entryEndDate = info['entryEndDate']
        startDate = info['startDate']
        endDate = info['endDate']
        minNumber = info['minNumber']
        maxNumber = info['maxNumber']
        typeID = info['typeID']
        clubID = info['clubID']
        description = info['description']
        area = info['area']
        createTime = info['createTime']
        fee = info['fee']
        activity = Activity(
            activityID=activityID, activityName=activityName, userID=userID,
            entryStartDate=entryStartDate, entryEndDate=entryEndDate, startDate=startDate,
            endDate=endDate, minNumber=minNumber, maxNumber=maxNumber,
            typeID=typeID, clubID=clubID, description=description,
            area=area, createTime=createTime, fee=fee
        )
        db.session.add(activity)
        return (True, None)


    @staticmethod
    def generate(result):
        res = {}
        res['activityID'] = result.activityID
        res['activityName'] = result.activityName
        res['description'] = result.description
        res['area'] = result.area
        res['fee'] = result.fee
        res['entryStartDate'] = str(result.entryStartDate)
        res['startDate'] = str(result.startDate)
        res['endDate'] = str(result.endDate)
        res['createTime'] = str(result.createTime)
        res['participateState'] = result.participateState
        return (True, res)

    @staticmethod
    def generateBrief(result):
        res = {}
        res['activityID'] = result.activityID
        res['activityName'] = result.activityName
        res['area'] = result.area
        res['createTime'] = str(result.createTime)
        res['participateState'] = result.participateState
        return (True, res)



