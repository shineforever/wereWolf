# coding=utf8
import base64
import hmac
import random
import re
import sys
sys.path.append('..')
# from Crypto.Cipher import AES


import hashlib
import time
import datetime
import oss2
import json
from functools import wraps

from tool.error_config import ErrorInfo
from tool.config import APP_ID
from tool.config import APP_SECRET
from tool.config import OSS_ACCESS_KEY_ID
from tool.config import OSS_ACCESS_KEY_SERCRET
from model.flaskapp import db
from model.token import Token

class Util:
    def __init__(self):
        pass

    @staticmethod
    def error_print(func):
        def wrapper(*args, **kwargs):
            '''
            关于数据库操作,输出错误日志
            :param args: 
            :param kwargs: 
            :return: 
            '''
            try:
                if kwargs:
                    return func(*args, kwargs)
                else:
                    return func(*args)
            except Exception as e:
                print(e)
                errorInfo = ErrorInfo['WOLFS_01']
                errorInfo['detail'] = str(e)
                db.session.rollback()
                return (False, errorInfo)
        return wrapper

    def _get_bucket(self, ossInfo, endpoint='oss-cn-beijing.aliyuncs.com'):
        bucket_str = ossInfo['bucket']
        auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SERCRET)
        _endpoint = endpoint
        return oss2.Bucket(auth, _endpoint, bucket_str)

    def upload_oss_image(self, info):
        bucket = self._get_bucket(info['oss_info'])
        img_name = info['img_name']
        img_file = info['img_file']
        return bucket.put_object(img_name, img_file)

    def get_security_url(self, oss_info):
        obj = oss_info['object_key']
        bucket = self._get_bucket(oss_info)
        return bucket.sign_url('GET', obj, 3600)

    def getCurrentTime(self):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        currentTime = time.strftime(ISOTIMEFORMAT, time.localtime())
        return currentTime

    def get_md5_string(self, str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    def generate_id(self, value):
        currentTime = self.getCurrentTime()
        now = datetime.datetime.now()
        resultID = self.get_md5_string(''.join([str(currentTime), value, str(now)]))
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
