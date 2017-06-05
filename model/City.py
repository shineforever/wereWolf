# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class City(db.Model):
    __tablename__ = 'City'
    cityID = db.Column(db.String(100), primary_key=True)
    cityName = db.Column(db.String(100))
    provinceID = db.Column(db.String(100), db.ForeignKey('Province.provinceID'))

    club = db.relationship('Club', backref='City', lazy='dynamic')
    county = db.relationship('County', backref='City', lazy='dynamic')

    def __repr__(self):
        return self.cityID

    @staticmethod
    def generate(result):
        res = {}
        res['cityID'] = result.cityID
        res['cityName'] = result.cityName
        return (True, res)