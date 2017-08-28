import sys
sys.path.append("..")
import json
from datetime import datetime

from tool.util import Util
from tool.error_config import ErrorInfo
from model.flaskapp import db
from model.token import Token

from tool.config import VALIDITY


class TokenManager(Util):

    def __init__(self):
        super().__init__()

    @Util.error_print
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
        db.session.commit()
        return (True, info['token_id'])

    @staticmethod
    @Util.error_print
    def check_admin_validity(func):
        '''
        验证后台登录信息
        第一步: 检查token是否存在;
        第二步: 检查token_id是否过期;
        第三步: 将token登录时间更新为最近的一次操作时间
        :param func: 
        :return: 
        '''
        def wrapper(*args):
            info = json.loads(args[1])
            token_id = info['token_id']
            query = db.session.query(Token).filter(Token.token_id == token_id)
            result = query.first()
            if not result:
                return (False, ErrorInfo['WOLFS_07'])
            createtime = result.createtime
            now = datetime.now()
            validity = result.validity
            days = (now - createtime).days
            if days > validity:
                return (False, ErrorInfo['WOLFS_05'])
            update_info = {Token.createtime: now}
            query.update(update_info, synchronize_session=False)
            db.session.commit()
            info['user_id'] = result.user_id
            return func(args[0], **info)
        return wrapper

    @staticmethod
    def checkUserValidity(func):
        def wrapper(*args):
            jsonInfo = args[1]
            info = json.loads(jsonInfo)
            # try:
            tokenID = info['tokenID']
            query = db.session.query(Token).filter(Token.tokenID == tokenID)
            result = query.first()
            if result is None:
                errorInfo = ErrorInfo['WOLFS_07']
                return (False, errorInfo)
            createTime = result.createTime
            now = datetime.now()
            validity = result.validity
            days = (now - createTime).days
            if days > validity:
                errorInfo = ErrorInfo['WOLFS_05']
                return (False, errorInfo)
            # 将token登录时间更新为最近的一次操作时间
            updateInfo = {Token.createTime: now}
            query.update(updateInfo, synchronize_session=False)
            db.session.commit()
            info['userID'] = result.userID
            return func(args[0], **info)
            # except Exception as e:
            #     print e
            #     errorInfo = ErrorInfo['WOLFS_01']
            #     errorInfo['detail'] = str(e)
            #     db.session.rollback()
            #     return (False, errorInfo)

        return wrapper



    # @staticmethod
    # def checkClubAdminValidity(func):
    #     def wrapper(*args):
    #         jsonInfo = args[1]
    #         info = json.loads(jsonInfo)
    #         try:
    #             tokenID = info['tokenID']
    #             query = db.session.query(Token).filter(Token.tokenID == tokenID)
    #             result = query.first()
    #             if result is None:
    #                 errorInfo = ErrorInfo['WOLFS_07']
    #                 return (False, errorInfo)
    #             createTime = result.createTime
    #             now = datetime.now()
    #             validity = result.validity
    #             days = (now - createTime).days
    #             if days > validity:
    #                 errorInfo = ErrorInfo['WOLFS_05']
    #                 return (False, errorInfo)
    #             # 将token登录时间更新为最近的一次操作时间
    #             updateInfo = {Token.createTime: now}
    #             query.update(updateInfo, synchronize_session=False)
    #             db.session.commit()
    #             userID = result.userID
    #             info['userID'] = userID
    #             clubQuery = db.session.query(Club).filter(Club.userID == userID)
    #             clubResult = clubQuery.first()
    #             info['clubID'] = clubResult.clubID
    #             info['area'] = clubResult.area
    #             return func(*args, **info)
    #         except Exception as e:
    #             print e
    #             errorInfo = ErrorInfo['WOLFS_01']
    #             errorInfo['detail'] = str(e)
    #             db.session.rollback()
    #             return (False, errorInfo)
    #
    #     return wrapper



    # def isTokenValid(self, info):
    #     #判断tokenID 是否存在
    #     try:
    #         tokenID = info['tokenID']
    #         query = db.session.query(Token).filter(Token.tokenID == tokenID)
    #         result = query.first()
    #         if result is None:
    #             errorInfo = ErrorInfo['WOLFS_07']
    #             return (False, errorInfo)
    #         createTime = result.createTime
    #         now = datetime.now()
    #         validity = result.validity
    #         days = (now - createTime).days
    #         if days > validity:
    #             errorInfo = ErrorInfo['WOLFS_05']
    #             return (False, errorInfo)
    #         #将token登录时间更新为最近的一次操作时间
    #         updateInfo = {Token.createTime : now}
    #         query.update(updateInfo, synchronize_session=False)
    #         db.session.commit()
    #         info['userID'] = result.userID
    #         return (True, result.userID)
    #     except Exception as e:
    #         print e
    #         errorInfo = ErrorInfo['WOLFS_01']
    #         errorInfo['detail'] = str(e)
    #         db.session.rollback()
    #         return (False, errorInfo)





if __name__ == '__main__':
    pass