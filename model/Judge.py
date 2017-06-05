# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db


class Judge(db.Model):
    __tablename__ = 'Judge'
    judgeID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100), db.ForeignKey('UserInfo.userID'))
    step = db.Column(db.Integer)
    description = db.Column(db.Text)
    createTime = db.Column(db.DateTime)
    reviewTime = db.Column(db.DateTime)

    def __init__(self, judgeID=None, userID=None, step=1,
                 description=None, createTime=None, reviewTime=None):
        self.judgeID = judgeID
        self.userID = userID
        self.step = step
        self.description = description
        self.createTime = createTime
        self.reviewTime = reviewTime

    def __repr__(self):
        return self.judgeID