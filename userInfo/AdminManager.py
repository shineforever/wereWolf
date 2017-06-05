# coding=utf8
import sys
import urllib2
import poster
import requests
sys.path.append("..")
import json
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import hashlib
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import or_
from datetime import datetime

from tool.Util import Util
from tool.errorConfig import ErrorInfo

from stoken.TokenManager import TokenManager
from model.flask_app import db
from model.AdminInfo import AdminInfo




class AdminManager(Util):

    def __init__(self):
        pass

    #管理员登录
    def adminLoginBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tel = info['tel']
        password = info['adminPW']
        adminPW = self.getMD5String(password)
        try:
            # 查询用户名或手机号是否已经存在
            query = db.session.query(AdminInfo).filter(
                        and_(
                            AdminInfo.tel == tel,
                            AdminInfo.adminPW == adminPW
                        )
                    )
            result = query.first()
            if result is None:
                errorInfo = ErrorInfo['WOLFS_03']
                return (False, errorInfo)
            tokenManager = TokenManager()
            tokenID = tokenManager.createToken(result.adminID)
            return (True, tokenID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 创建管理员
    def createAdminInfoBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        print 'create', info
        adminName = info['adminName']
        password = info['adminPW']
        tel = info['tel']
        try:
            # 查询用户名或手机号是否已经存在
            query = db.session.query(AdminInfo).filter(
                or_(AdminInfo.adminName == adminName,
                    AdminInfo.tel == tel)
            )
            result = query.first()
            if result is not None:
                errorInfo = ErrorInfo['WOLFS_02']
                errorInfo['detail'] = str(result)
                return (False, errorInfo)

            info['adminID'] = self.generateID(tel)
            info['adminPW'] = self.getMD5String(password)
            AdminInfo.create(info=info)
            db.session.commit()
            return (True, info['adminID'])
        except Exception as e:
            print e
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)



    # 管理员身份验证, 如果身份校验成功,返回管理员ID
    def adminAuth(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, userID)
        try:
            # 该userID是否是管理员
            query = db.session.query(AdminInfo).filter(AdminInfo.adminID==userID)
            result = query.first()
            if result is None:
                errorInfo = ErrorInfo['WOLFS_06']
                return (False, errorInfo)
            return (True, userID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)



if __name__ == '__main__':
    pass