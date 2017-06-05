# coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import json
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import and_
from tool.errorConfig import ErrorInfo
from tool.config import ACTIVITY_CLUB
from tool.config import ACTIVITY_USER
from tool.Util import Util
from userInfo.AdminManager import AdminManager
from image.ImageManager import ImageManager
from stoken.TokenManager import TokenManager

from model.flask_app import db
from model.Activity import Activity
from model.ImgPath import ImgPath
from model.UserInfo import UserInfo
from model.Club import Club
from model.Participate import Participate


class ActivityManager(Util):

    def __init__(self):
        pass

    # 后台，　创建活动
    def createActivityBackground(self, jsonInfo, imgFile):
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
            Activity.create(info=info)
            db.session.commit()
            return (True, info['clubID'])
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 创建活动
    def createActivity(self, jsonInfo, imgFile):
        info = json.loads(jsonInfo)
        try:
            # 管理员身份校验
            # 管理员身份校验
            tokenManager = TokenManager()
            (status, userID) = tokenManager.isTokenValid(info=info)
            if status is not True:
                return (False, userID)
            # 图片上传
            ossInfo = {}
            ossInfo['bucket'] = 'sjsecondhand'
            imgName = imgFile.filename
            _l = imgName.split(".")
            if len(_l) > 0:
                postfix = _l[-1]
            else:
                postfix = 'png'
            info['activityID'] = self.generateID(info['activityName'])
            info['imgPathID'] = self.generateID(imgName)
            info['path'] = info['imgPathID'] + '.' + postfix
            info['foreignID'] = info['activityID']
            self.uploadOSSImage('merchandise/%s' % info['path'], ossInfo, imgFile)
            ImgPath.create(info=info)
            info['createTime'] = datetime.now()
            info['entryEndDate'] = info['entryStartDate']
            info['maxNumber'] = None
            if info.has_key('clubID'):
                info['typeID'] = ACTIVITY_CLUB
                info['area'] = None
            else:
                info['clubID'] = None
                info['typeID'] = ACTIVITY_USER
            Activity.create(info=info)
            db.session.commit()
            return (True, info['activityID'])
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 获取活动详情
    def getActivityDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        try:
            # 身份校验
            tokenManager = TokenManager()
            (status, userID) = tokenManager.isTokenValid(info=info)
            if status is not True:
                return (False, userID)
            return self._generateActivityDetail(info=info)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)



    def _generateActivityDetail(self, info):
        activityID = info['activityID']
        query = db.session.query(Activity, Club).outerjoin(
            Club, Activity.clubID == Club.clubID
        ).filter(Activity.activityID == activityID)
        result = query.first()
        if result is None:
            errorInfo = ErrorInfo['WOLFS_09']#不存在该活动
            return (False, errorInfo)
        callBackData = {}
        if result.Club is not None:
            (status, clubInfo) = Club.generateBrief(result=result.Club)
            callBackData['address'] = clubInfo['area']
            callBackData.update(clubInfo)
        (status, activityInfo) = Activity.generate(result=result.Activity)
        if activityInfo['area'] is not None:
            callBackData['address'] = activityInfo['area']
        callBackData.update(activityInfo)
        imageManager = ImageManager()
        info['foreignID'] = activityID
        (status, imgInfo) = imageManager.getImage(info=info)
        callBackData.update(imgInfo)
        return (True, callBackData)

    # 获取普通活动列表
    def getUserActivityList(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['typeID'] = ACTIVITY_USER
        return self._generateActivityList(info=info)

    # 获取俱乐部活动列表
    def getClubActivityList(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['typeID'] = ACTIVITY_CLUB
        return self._generateActivityList(info=info)

    def _generateActivityList(self, info):
        typeID = info['typeID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        if typeID == ACTIVITY_USER:
            query = db.session.query(Activity).filter(Activity.typeID == ACTIVITY_USER)
            allResult = query.order_by(desc(Activity.createTime)).offset(startIndex).limit(pageCount).all()
            def generateInfo(result):
                res = {}
                (status, activityInfo) = Activity.generateBrief(result)
                res.update(activityInfo)
                return res
            callBackData = [generateInfo(result=result) for result in allResult]
        else:
            query = db.session.query(Activity, Club).outerjoin(
                Club, Activity.clubID == Club.clubID
            ).filter(Activity.typeID == ACTIVITY_CLUB)
            allResult = query.order_by(desc(Activity.createTime)).offset(startIndex).limit(pageCount).all()
            def generateInfo(result):
                res = {}
                (status, activityInfo) = Activity.generateBrief(result.Activity)
                res.update(activityInfo)
                (status, clubInfo) = Club.generateBrief(result.Club)
                res.update(clubInfo)
                return res
            callBackData = [generateInfo(result=result) for result in allResult]
        return (True, callBackData)


    def createParticipate(self, jsonInfo):
        info = json.loads(jsonInfo)
        activityID = info['activityID']
        try:
            # 身份校验
            tokenManager = TokenManager()
            (status, userID) = tokenManager.isTokenValid(info=info)
            if status is not True:
                return (False, userID)
            #活动是否存在，是否已经加入,是否已经满员
            query = db.session.query(Activity).filter(
                Activity.activityID == activityID
            )
            result = query.first()
            if result is None:
                errorInfo = ErrorInfo['WOLFS_09']  # 不存在该活动
                return (False, errorInfo)
            userQuery = db.session.query(Participate).filter(
                and_(
                    Participate.activityID == activityID,
                    Participate.userID == userID
                )
            )
            userResult = userQuery.first()
            if userResult is not None:
                errorInfo = ErrorInfo['WOLFS_11']  #已经报名
                return (False, errorInfo)
            participateQuery = db.session.query(func.count(Participate.participateID)).filter(
                Participate.activityID == activityID
            )
            participateCount = participateQuery.first()[0]
            activityCount = result.minNumber
            if participateCount + 1 > activityCount:
                errorInfo = ErrorInfo['WOLFS_10']  # 活动报名人数已满
                return (False, errorInfo)
            elif (participateCount + 1 == activityCount):
                updateInfo = {Activity.participateState: False}
                query.update(updateInfo, synchronize_session=False)
            info['participateID'] = self.generateID(userID + activityID)
            info['createTime'] = datetime.now()
            Participate.create(info=info)
            db.session.commit()
            return (True, info['participateID'])
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)






