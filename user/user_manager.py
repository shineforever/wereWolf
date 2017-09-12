import hashlib
import sys
import requests

sys.path.append("..")
from datetime import datetime
import json
from sqlalchemy import and_
from sqlalchemy import or_

from tool.util import Util
from tool.error_config import ErrorInfo
from stoken.token_manager import TokenManager
from model.flaskapp import db
from model.userinfo import UserInfo
from model.token import Token
from model.imgpath import ImgPath
from model.participate import Participate
from model.activity import Activity

from tool.config import VALIDITY
from tool.config import APP_ID
from tool.config import APP_SECRET
from tool.config import GET_OPENID_URL

class UserManager(Util):

    def __init__(self):
        super().__init__()

    @TokenManager.check_admin_validity
    @Util.error_print
    def create_user_background(self, info):
        '''
        后台，创建用户
        第一步: 验证管理员身份
        第二步: 创建Token, Imgpath, UserInfo信息
        :param info: {'token_id': '', 'user_name': '', 'imgpath': '', 'user_id': '', 'open_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        info['user_id'] = self.generate_id(info['user_name'])
        info['token_id'] = self.generate_id(info['user_id'])
        info['createtime'] = datetime.now()
        info['validity'] = VALIDITY
        Token.create(info)
        info['imgpath_id'] = self.generate_id(info['imgpath'])
        info['imgpath'] = info['imgpath']
        info['foreign_id'] = info['user_id']
        ImgPath.create(info=info)
        UserInfo.create(info=info)
        db.session.commit()
        return (True, info['user_id'])

    @Util.error_print
    def _create_user(self, info):
        '''
        后台，创建用户
        第一步: 验证管理员身份
        第二步: 创建Token, Imgpath, UserInfo信息
        :param info: {'token_id': '', 'user_name': '', 'imgpath': '', 'user_id': '', 'open_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        info['imgpath_id'] = self.generate_id(info['imgpath'])
        info['imgpath'] = info['imgpath']
        info['foreign_id'] = info['user_id']
        ImgPath.create(info=info)
        UserInfo.create(info=info)
        db.session.commit()
        return (True, info['user_id'])

    def _update_user_info(self, info):
        '''
        变更用户信息
        微信重新登录后，验证用户的头像或者昵称是否变化，如果变化，修改信息
        :param info:
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        foreign_id = info['foreign_id']
        imgpath = info['imgpath']
        user_name = info['user_name']
        query = db.session.query(ImgPath).filter(ImgPath.foreign_id == foreign_id)
        user_query = db.session.query(UserInfo).filter(UserInfo.user_id == foreign_id)
        user_result = user_query.first()
        result = query.first()
        if user_result.user_name != user_name:
            user_query.update({UserInfo.user_name == user_name}, synchronize_session=False)
        if result.imgpath != imgpath:
            query.update({ImgPath.imgpath == imgpath}, synchronize_session=False)
        return (True, None)

    # @Util.error_print
    def wechat_login(self, jsonInfo):
        '''
        微信用户登录
        第一步:# 获取唯一的open_id
        第二步: 判断用户是否是第一次登录，如果是，则创建用户信息，否则，查看是否需要变更用户信息
        :param info: 
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        info = json.loads(jsonInfo)
        raw_data = info['rawData'].encode('utf-8')
        signature = info['signature']
        code = info['code']
        url = GET_OPENID_URL
        payload = {'appid': APP_ID, 'secret': APP_SECRET, 'js_code': code, 'grant_type': 'authorization_code'}
        r = requests.get(url=url, params=payload)
        ret = json.loads(r.text)
        open_id = ret['openid']
        session_key = ret['session_key'].encode('utf-8')
        new_signature = hashlib.sha1(raw_data + session_key).hexdigest()
        if signature == new_signature:
            query = db.session.query(UserInfo).filter(UserInfo.open_id == open_id)
            result = query.first()
            user_info = {}
            raw_data_dict = json.loads(info['rawData'])
            avatar_url = raw_data_dict['avatarUrl']
            user_name = raw_data_dict['nickName']
            user_info['imgpath'] = avatar_url
            user_info['open_id'] = open_id
            user_info['user_name'] = user_name


            if result:
                user_info['user_id'] = result.user_id
                user_info['foreign_id'] = user_info['user_id']
                self._update_user_info(user_info)
            else:
                user_info['user_id'] = self.generate_id(open_id)
                user_info['imgpath_id'] = self.generate_id(avatar_url)
                user_info['foreign_id'] = user_info['user_id']
                user_info['createtime'] = datetime.now()
                ImgPath.create(info=user_info)
                UserInfo.create(info=user_info)
            tokenManager = TokenManager()
            user_info['validity'] = VALIDITY
            (status, token_id) = tokenManager.update_token(info=user_info)
            db.session.commit()
            return (True, token_id)
        else:
            return (False, None)





if __name__ == '__main__':
    pass