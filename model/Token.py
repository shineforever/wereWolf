# coding:utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Token(db.Model):
    __tablename__ = 'Token'
    tokenID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    validity = db.Column(db.Text)

    def __init__(self, tokenID=None, userID=None, createTime=None, validity=None):
        self.tokenID = tokenID
        self.userID = userID
        self.createTime = createTime
        self.validity = validity

    @staticmethod
    def create(info):
        tokenID = info['tokenID']
        userID = info['userID']
        createTime = info['createTime']
        validity = info['validity']
        token = Token(tokenID=tokenID, userID=userID, createTime=createTime, validity=validity)
        db.session.add(token)
        return (True, None)

    def __repr__(self):
        return self.tokenID