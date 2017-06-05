# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from datetime import datetime
from tool.Util import Util
from tool.errorConfig import ErrorInfo

from model.flask_app import db
from model.Token import Token


class TokenManager(Util):
    def __init__(self):
        pass

    def createToken(self, userID):
        try:
            db.session.query(Token).filter(
                Token.userID == userID
            ).delete(synchronize_session=False)
            info = {}
            info['tokenID'] = self.generateID(userID)
            info['userID'] = userID
            info['createTime'] = datetime.now()
            info['validity'] = 7
            Token.create(info=info)
            db.session.commit()
            return info['tokenID']
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def isTokenValid(self, info):
        #判断tokenID 是否存在
        try:
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
            #将token登录时间更新为最近的一次操作时间
            updateInfo = {Token.createTime : now}
            query.update(updateInfo, synchronize_session=False)
            db.session.commit()
            info['userID'] = result.userID
            return (True, result.userID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['WOLFS_01']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)





if __name__ == '__main__':
    pass