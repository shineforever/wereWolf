# coding=utf8
import base64
import hmac
import random
import re
import sys
from Crypto.Cipher import AES

sys.path.append('..')
import hashlib
import time
import datetime
import oss2
import json

from errorConfig import ErrorInfo
from tool.config import APP_ID
from tool.config import APP_SECRET
from model.flask_app import db
from model.Token import Token

class Util:
    def __init__(self):
        pass

    def _getBucket(self, ossInfo, endpoint='oss-cn-hangzhou.aliyuncs.com'):
        bucketStr = ossInfo['bucket']
        OSSAccessKeyId = 'HReEC1sQufBRLcQC'
        secret = '5rqWY7jXhGeF0HBhYpl10mSkgrrHZt'
        auth = oss2.Auth(OSSAccessKeyId, secret)
        _endpoint = endpoint
        return oss2.Bucket(auth, _endpoint, bucketStr)


    def uploadOSSImage(self, imageName, ossInfo, imgFile):
        bucket = self._getBucket(ossInfo)
        return bucket.put_object(imageName, imgFile)

    def getSecurityUrl(self, ossInfo):
        obj = ossInfo['objectKey']
        bucket = self._getBucket(ossInfo, endpoint='img-cn-hangzhou.aliyuncs.com')
        return bucket.sign_url('GET', obj, 3600)

    def getCurrentTime(self):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        currentTime = time.strftime(ISOTIMEFORMAT, time.localtime())
        return currentTime

    def getMD5String(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def generateID(self, value):
        currentTime = self.getCurrentTime()
        now = datetime.datetime.now()
        resultID = self.getMD5String(''.join([str(currentTime), value, str(now)]))
        resultID = ''.join([str(currentTime), resultID]).replace(' ','')
        resultID = ''.join(re.split(':', resultID))
        return resultID


    def isTokenValid(self, tokenID):
        #判断tokenID 是否存在
        try:
            query = db.session.query(Token).filter(Token.tokenID==tokenID)
            result = query.first()
            if result is None:
                errorInfo = ErrorInfo['WOLFS_04']
                return (False, errorInfo)
            createTime = result.createTime
            now = datetime.datetime.now()
            days = (now - createTime).days
            validity = result.validity
            if days > validity:
                errorInfo = ErrorInfo['WOLFS_05']
                errorInfo['detail'] = result
                return (False, errorInfo)
            #将token登录时间更新为最近的一次操作时间
            updateInfo = {Token.createTime : now}
            query.update(updateInfo,synchronize_session=False)
            db.session.commit()
            return (True, result.userID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    #微信登录时候，解密用户加密的数据信息
    def decrypt(self, encryptedData, iv, sessionKey):
        # base64 decode
        sessionKey = base64.b64decode(sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != APP_ID:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]





if __name__ == '__main__':
    u = Util()
    print u.generateID('a')
