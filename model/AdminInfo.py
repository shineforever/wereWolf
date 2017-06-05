#coding:utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db


class AdminInfo(db.Model):
    __tablename__ = 'AdminInfo'
    adminID = db.Column(db.String(100), primary_key=True)
    adminPW = db.Column(db.String(100))
    adminName = db.Column(db.String(100))
    tel = db.Column(db.String(100))

    def __init__(self, adminID=None, adminName=None, adminPW=None, tel=None):
        self.adminID = adminID
        self.adminName = adminName
        self.adminPW = adminPW
        self.tel = tel


    @staticmethod
    def create(info):
        adminID = info['adminID']
        adminName = info['adminName']
        adminPW = info['adminPW']
        tel = info['tel']
        adminInfo = AdminInfo(adminID=adminID, adminName=adminName,
                              adminPW=adminPW, tel=tel)
        db.session.add(adminInfo)
        return (True, None)

    def __repr__(self):
        return self.adminID