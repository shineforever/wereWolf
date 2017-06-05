# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class ImgPath(db.Model):
    __tablename__ = 'ImgPath'
    imgPathID = db.Column(db.String(100), primary_key=True)
    path = db.Column(db.String(1000))
    foreignID = db.Column(db.String(100))

    def __init__(self, imgPathID=None, path=None, foreignID=None):
        self.imgPathID = imgPathID
        self.path = path
        self.foreignID = foreignID

    def __repr__(self):
        return self.imgPathID

    @staticmethod
    def create(info):
        imgPathID = info['imgPathID']
        path = info['path']
        foreignID = info['foreignID']
        imgPath = ImgPath(imgPathID=imgPathID, path=path, foreignID=foreignID)
        db.session.add(imgPath)
        return (True, None)