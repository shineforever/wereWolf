import sys
sys.path.append("..")
import json
from datetime import datetime

from tool.util import Util
from tool.error_config import ErrorInfo
from model.flaskapp import db
from model.token import Token
from model.admininfo import AdminInfo
from model.userinfo import UserInfo

from tool.config import VALIDITY


class TokenManager(Util):

    def __init__(self):
        super().__init__()

    def update_token(self, info):
        user_id = info['user_id']
        db.session.query(Token).filter(
            Token.user_id == user_id
        ).delete(synchronize_session=False)
        info = {}
        info['token_id'] = self.generate_id(user_id)
        info['user_id'] = user_id
        info['createtime'] = datetime.now()
        info['validity'] = VALIDITY
        Token.create(info=info)
        return (True, info['token_id'])

    @staticmethod
    def check_admin_validity(func):
        '''
        验证后台登录信息
        第一步: 检查token是否存在;
        第二步: 检查token_id是否过期;
        第三步: 将token登录时间更新为最近的一次操作时间
        :param func: 
        :return: 
        '''
        @Util.error_print
        def wrapper(*args):
            info = json.loads(args[1])
            token_id = info['token_id']
            query = db.session.query(Token, AdminInfo).outerjoin(
                AdminInfo,  Token.user_id == AdminInfo.admin_id
            ).filter(Token.token_id == token_id)
            result = query.first()
            if not result:
                return (False, ErrorInfo['WOLFS_07'])
            result = result.Token
            createtime = result.createtime
            now = datetime.now()
            validity = result.validity
            days = (now - createtime).days
            if days > validity:
                return (False, ErrorInfo['WOLFS_05'])
            result.createtime = now
            db.session.commit()
            info['user_id'] = result.user_id
            return func(args[0], info)
        return wrapper

    @staticmethod
    def check_user_validity(func):
        '''
        验证用户登录信息
        第一步: 检查token是否存在;
        第二步: 检查token_id是否过期;
        第三步: 将token登录时间更新为最近的一次操作时间
        :param func: 
        :return: 
        '''
        # @Util.error_print
        def wrapper(*args):
            info = json.loads(args[1])
            token_id = info['token_id']
            query = db.session.query(Token, UserInfo).outerjoin(
                UserInfo,  Token.user_id == UserInfo.user_id
            ).filter(Token.token_id == token_id)
            result = query.first()
            if not result:
                return (False, ErrorInfo['WOLFS_07'])
            result = result.Token
            createtime = result.createtime
            now = datetime.now()
            validity = result.validity
            days = (now - createtime).days
            if days > validity + 30:
                return (False, ErrorInfo['WOLFS_05'])
            result.createtime = now
            db.session.commit()
            info['user_id'] = result.user_id
            return func(args[0], info)
        return wrapper






if __name__ == '__main__':
    pass