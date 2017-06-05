#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Club(db.Model):
    __tablename__ = 'Club'
    clubID = db.Column(db.String(100), primary_key=True)
    clubName = db.Column(db.String(100))
    creatorName = db.Column(db.String(100))
    userID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    provinceID = db.Column(db.String(100), db.ForeignKey('Province.provinceID'))
    cityID = db.Column(db.String(100), db.ForeignKey('City.cityID'))
    countyID = db.Column(db.String(100), db.ForeignKey('County.countyID'))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    area = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, clubID=None, clubName=None, creatorName=None,
                 userID=None, provinceID=None, cityID=None,
                 countyID=None, area=None, longitude=118.46,
                 latitude=32.03, createTime=None):
        self.clubID = clubID
        self.clubName = clubName
        self.creatorName = creatorName
        self.userID = userID
        self.provinceID = provinceID
        self.cityID = cityID
        self.countyID = countyID
        self.area = area
        self.longitude = longitude
        self.latitude = latitude
        self.createTime = createTime

    def __repr__(self):
        return self.clubID

    @staticmethod
    def create(info):
        clubID = info['clubID']
        clubName = info['clubName']
        creatorName = info['creatorName']
        userID = info['userID']
        provinceID = info['provinceID']
        cityID = info['cityID']
        countyID = info['countyID']
        area = info['area']
        createTime = info['createTime']
        longitude = info['longitude']
        latitude = info['latitude']
        club = Club(
            clubID=clubID, clubName=clubName, creatorName=creatorName,
            userID=userID, provinceID=provinceID, cityID=cityID,
            countyID=countyID, area=area, longitude=longitude,
            latitude=latitude, createTime=createTime
        )
        db.session.add(club)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['clubID'] = result.clubID
        res['clubName'] = result.clubName
        res['creatorName'] = result.creatorName
        res['longitude'] = result.longitude
        res['latitude'] = result.latitude
        res['area'] = result.area
        res['createTime'] = str(result.createTime)
        return (True, res)

    @staticmethod
    def generateBrief(result):
        res = {}
        res['clubID'] = result.clubID
        res['clubName'] = result.clubName
        res['area'] = result.area
        return (True, res)

