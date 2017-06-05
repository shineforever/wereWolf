# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class County(db.Model):
    __tablename__ = 'County'
    countyID = db.Column(db.String(100), primary_key=True)
    countyName = db.Column(db.String(100))
    cityID = db.Column(db.String(100), db.ForeignKey('City.cityID'))
    zipCode = db.Column(db.String(100))

    club = db.relationship('Club', backref='County', lazy='dynamic')

    def __init__(self, countyID=None, countyName=None,
                 cityID=None, zipCode=None):
        self.countyID = countyID
        self.countyName = countyName
        self.cityID = cityID
        self.zipCode = zipCode

    def __repr__(self):
        return self.countyID

    @staticmethod
    def generate(result):
        res = {}
        res['countyID'] = result.countyID
        res['countyName'] = result.countyName
        res['zipCode'] = result.zipCode
        return (True, res)
