# coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import json
from datetime import datetime
from tool.errorConfig import ErrorInfo
from tool.Util import Util
from userInfo.AdminManager import AdminManager
from image.ImageManager import ImageManager
from stoken.TokenManager import TokenManager

from model.flask_app import db
from model.Club import Club
from model.ImgPath import ImgPath
from model.City import City
from model.County import County
from model.Province import Province
from model.UserInfo import UserInfo


class ClubManager(Util):

    def __init__(self):
        pass

    # 后台，　创建俱乐部
    def createClubBackground(self, jsonInfo, imgFile):
        info = json.loads(jsonInfo)
        try:
            # 管理员身份校验
            adminManager = AdminManager()
            (status, reason) = adminManager.adminAuth(jsonInfo)
            if status is not True:
                return (False, reason)
            # 头像上传
            ossInfo = {}
            ossInfo['bucket'] = 'sjsecondhand'
            imgName = imgFile.filename
            _l = imgName.split(".")
            if len(_l) > 0:
                postfix = _l[-1]
            else:
                postfix = 'png'
            info['clubID'] = self.generateID(info['clubName'])
            info['imgPathID'] = self.generateID(imgName)
            info['path'] = info['imgPathID'] + '.' + postfix
            info['foreignID'] = info['clubID']
            self.uploadOSSImage('merchandise/%s' % info['path'], ossInfo, imgFile)
            ImgPath.create(info=info)
            info['createTime'] = datetime.now()
            if not info.has_key('userID'):
                info['userID'] = None
            Club.create(info=info)
            db.session.commit()
            return (True, info['clubID'])
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 后台，　获取俱乐部详情
    def getClubDetailBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        try:
            # 管理员身份校验
            adminManager = AdminManager()
            (status, reason) = adminManager.adminAuth(jsonInfo)
            if status is not True:
                return (False, reason)
            return self._generateClubDetail(info=info)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 获取俱乐部详情
    def getClubDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        try:
            # 身份校验
            tokenManager = TokenManager()
            (status, userID) = tokenManager.isTokenValid(info=info)
            if status is not True:
                return (False, userID)
            return self._generateClubDetail(info=info)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)


    def _generateClubDetail(self, info):
        clubID = info['clubID']
        query = db.session.query(Club, UserInfo, Province, City, County).outerjoin(
            UserInfo, Club.userID == UserInfo.userID
        ).outerjoin(
            Province, Club.provinceID == Province.provinceID
        ).outerjoin(
            City, Club.cityID == City.cityID
        ).outerjoin(
            County, Club.countyID == County.countyID
        ).filter(Club.clubID == clubID)
        result = query.first()
        if result is None:
            errorInfo = ErrorInfo['WOLFS_08']
            return (False, errorInfo)
        callBackData = {}
        if result.UserInfo is not None:
            (status, userInfo) = UserInfo.generate(result=result.UserInfo)
            callBackData.update(userInfo)
        (status, provinceInfo) = Province.generate(result=result.Province)
        (status, cityInfo) = City.generate(result=result.City)
        (status, countyInfo) = County.generate(result=result.County)
        (status, clubInfo) = Club.generate(result=result.Club)
        callBackData.update(provinceInfo)
        callBackData.update(cityInfo)
        callBackData.update(countyInfo)
        callBackData.update(clubInfo)
        imageManager = ImageManager()
        info['foreignID'] = clubID
        (status, imgInfo) = imageManager.getImage(info=info)
        callBackData.update(imgInfo)
        return (True, callBackData)