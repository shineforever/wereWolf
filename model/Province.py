# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db


class Province(db.Model):
    __tablename__ = 'Province'
    provinceID = db.Column(db.String(100), primary_key=True)
    provinceName = db.Column(db.String(100))

    city = db.relationship('City', backref='Province', lazy='dynamic')
    club = db.relationship('Club', backref='Province', lazy='dynamic')

    def __repr__(self):
        return self.provinceID

    @staticmethod
    def generate(result):
        res = {}
        res['provinceID'] = result.provinceID
        res['provinceName'] = result.provinceName
        return (True, res)