import sys
sys.path.append("..")
from datetime import datetime
import json
from sqlalchemy import and_
from sqlalchemy import or_

from tool.util import Util
from tool.error_config import ErrorInfo
from stoken.token_manager import TokenManager
from model.flaskapp import db
from model.admininfo import AdminInfo
from model.token import Token

from tool.config import VALIDITY

class AdminManager(Util):

    def __init__(self):
        super().__init__()

    @Util.error_print
    def create_admin_info_background(self, jsonInfo):
        '''
        创建管理员
        第一步:检查是否已经创建过(根据用户名或手机号);
        第二步:创建token
        第三步:创建admininfo
        :param jsonInfo: {'password': '', 'admin_name': '', 'tel': ''}
        :return: {'status': 'SUCCESS', 'data': ''}
        '''
        info = json.loads(jsonInfo)
        admin_name = info['admin_name']
        tel = info['tel']
        password = info['password']
        query = db.session.query(AdminInfo).filter(
            or_(AdminInfo.admin_name == admin_name,
                AdminInfo.tel == tel)
        )
        result = query.first()
        if result:
            return (False, ErrorInfo['WOLFS_02'])
        info['admin_id'] = self.generate_id(tel)
        info['password'] = self.get_md5_string(password)
        info['token_id'] = self.generate_id(info['admin_id'])
        info['user_id'] = info['admin_id']
        info['createtime'] = datetime.now()
        info['validity'] = VALIDITY
        Token.create(info=info)
        AdminInfo.create(info=info)
        db.session.commit()
        return (True, info['admin_id'])

    @Util.error_print
    def admin_login_background(self, jsonInfo):
        '''
        管理员登录
        第一步: 查询管理员是否已经存在(根据用户名或手机号)
        :param jsonInfo: {'tel': '', 'password': ''}
        :return: {'status': 'SUCCESS', 'data': ''}
        '''
        info = json.loads(jsonInfo)
        tel = info['tel']
        password = self.get_md5_string(info['password'])
        query = db.session.query(AdminInfo).filter(
            and_(
                AdminInfo.tel == tel,
                AdminInfo.password == password
            )
        )
        result = query.first()
        info['user_id'] = result.admin_id
        if result is None:
            errorInfo = ErrorInfo['WOLFS_03']
            return (False, errorInfo)
        tokenManager = TokenManager()
        (status, token_id) = tokenManager.update_token(info)
        if status is False:
            return (False, token_id)
        return (True, token_id)

    # # 管理员身份验证, 如果身份校验成功,返回管理员ID
    # def adminAuth(self, jsonInfo):
    #     info = json.loads(jsonInfo)
    #     tokenID = info['tokenID']
    #     (status, userID) = self.isTokenValid(tokenID)
    #     if status is not True:
    #         return (False, userID)
    #     try:
    #         # 该userID是否是管理员
    #         query = db.session.query(AdminInfo).filter(AdminInfo.adminID==userID)
    #         result = query.first()
    #         if result is None:
    #             errorInfo = ErrorInfo['WOLFS_06']
    #             return (False, errorInfo)
    #         return (True, userID)
    #     except Exception as e:
    #         errorInfo = ErrorInfo['WOLFS_01']
    #         errorInfo['detail'] = str(e)
    #         db.session.rollback()
    #         return (False, errorInfo)



if __name__ == '__main__':
    pass