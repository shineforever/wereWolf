# coding=utf8
import sys
import urllib
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
from tool.config import APP_ID
from tool.config import APP_SECRET
from tool.config import WECHAT_USER_TAG
from userInfo.AdminManager import AdminManager
from image.ImageManager import ImageManager
from stoken.TokenManager import TokenManager


from model.flask_app import db
from model.ImgPath import ImgPath
from model.UserInfo import UserInfo
from model.Club import Club
from model.Judge import Judge


class UserInfoManager(Util):

    def __init__(self):
        pass

    # 后台，创建用户
    def createUserBackground(self, jsonInfo, imgFile):
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
            userID = self.generateID(info['userName'])
            tokenManager = TokenManager()
            tokenManager.createToken(userID)
            info['userID'] = userID
            info['imgPathID'] = self.generateID(imgName)
            info['path'] = info['imgPathID'] + '.' + postfix
            info['foreignID'] = userID
            self.uploadOSSImage('merchandise/%s' % info['path'], ossInfo, imgFile)
            ImgPath.create(info=info)
            info['createTime'] = datetime.now()
            UserInfo.create(info=info)
            db.session.commit()
            return (True, userID)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 后台，获取用户详情
    def getUserInfoDetailBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        try:
            # 管理员身份校验
            adminManager = AdminManager()
            (status, reason) = adminManager.adminAuth(jsonInfo)
            if status is not True:
                return (False, reason)
            return self._generateUserDetail(info=info)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 后台，获取用户详情
    def getUserInfoDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        try:
            # 管理员身份校验
            tokenManager = TokenManager()
            (status, userID) = tokenManager.isTokenValid(info=info)
            if status is not True:
                return (False, userID)
            return self._generateUserDetail(info=info)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 后台，获取用户列表
    def getUserListBackground(self, jsonInfo):
        return (True, None)

    #微信小程序，登录
    def loginWithWechat(self, jsonInfo):
        info = json.loads(jsonInfo)
        try:
            (status, resultDict) = self.getWechatResult(info=info)
            if status is True:
                tokenManager = TokenManager()
                tokenID = tokenManager.createToken(info['openID'])
                # 查询是否存在已经创建的用户
                query = db.session.query(UserInfo).filter(UserInfo.openID == info['openID'])
                result = query.first()
                if result is None:
                    (status, callBackData) = self.createWechatUser(info=info, resultDict=resultDict)
                    db.session.commit()
                return (True, tokenID)
            else:
                return (False, None)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def getWechatResult(self, info):
        encryptedData = info['encryptedData']
        rawData = str(info['rawData'])
        signature = info['signature']
        iv = info['iv']
        # 第一步：获取参数code, encryptedData, rawData, signature, iv
        code = info['code']
        # 第二步：　获取唯一的openid, session_key
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s' \
              '&secret=%s&js_code=%s&grant_type=authorization_code' % (APP_ID, APP_SECRET, code)
        f = urllib.urlopen(url)
        ret = json.loads(f.read())
        if (len(ret['session_key']) > 1 and len(ret['openid']) > 1):
            # 第三步：根据openid, 生成tokenID, 将tokenID, session_key 存入到数据库中
            info['openID'] = ret['openid']
            sessionKey = ret['session_key']
            sessionKey = str(sessionKey)
            # 第四步，　验证签名
            newSignature = hashlib.sha1(rawData + sessionKey).hexdigest()
            if newSignature == signature:
                encryptedData = encryptedData.encode('utf-8')
                resultDict = self.decrypt(encryptedData, iv, sessionKey)
                return (True, resultDict)
        return (False, None)


    def createWechatUser(self, info, resultDict):
        # 不能存储微信头像的url，因为：1，如果头像更换后，将无法获取
        # 2，其他地方获取用户头像时，会作oss转换，导致无法显示
        info['userID'] = self.generateID(info['openID'])
        info['userName'] = resultDict['nickName']
        info['createTime'] = datetime.now()
        info['gender'] = resultDict['gender']
        info['userType'] = WECHAT_USER_TAG
        info['longitude'] = ''
        info['latitude'] = ''
        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        try:
            f = urllib2.urlopen(resultDict['avatarUrl'])
            imgFile = f.read()
            imgName = self.generateID(info['userName']) + '.png'
            self.uploadOSSImage('portrait/%s' % imgName, ossInfo, imgFile)
            info['imgPathID'] = self.generateID(imgName)
            info['path'] = imgName
            info['foreignID'] = info['userID']
            ImgPath.create(info=info)
            UserInfo.create(info=info)
            return (True, None)
        except Exception as e:
            print e
            db.session.rollback()
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def _generateUserDetail(self, info):
        userID = info['userID']
        query = db.session.query(UserInfo).filter(UserInfo.userID == userID)
        result = query.first()
        if result is None:
            errorInfo = ErrorInfo['WOLFS_03']
            return (False, errorInfo)
        (status, callBackData) = UserInfo.generate(result=result)
        imageManager = ImageManager()
        info['foreignID'] = userID
        (status, imgInfo) = imageManager.getImage(info=info)
        callBackData.update(imgInfo)
        return (True, callBackData)

if __name__ == '__main__':
    pass