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
from model.club import Club
from model.imgpath import ImgPath




class ClubManager(Util):

    def __init__(self):
        super().__init__()

    # 后台，　创建俱乐部
    @TokenManager.check_admin_validity
    @Util.error_print
    def create_club_background(self, info):
        '''
        后台，　创建俱乐部
        第一步: 验证该俱乐部是否已经存在(根据俱乐部名称);
        第二步: 创建俱乐部图片;
        第三步: 创建俱乐部
        :param info: 
        :return: 
        '''
        info['club_id'] = self.generate_id(info['club_name'])
        info['imgpath'] = info['imgpath']
        info['imgpath_id'] = self.generate_id(info['imgpath'])
        info['foreign_id'] = info['club_id']
        info['createtime'] = datetime.now()
        ImgPath.create(info=info)
        Club.create(info=info)
        db.session.commit()
        return (True, info['club_id'])

    # # 后台，　获取俱乐部详情
    # def getClubDetailBackground(self, jsonInfo):
    #     info = json.loads(jsonInfo)
    #     try:
    #         # 管理员身份校验
    #         adminManager = AdminManager()
    #         (status, reason) = adminManager.adminAuth(jsonInfo)
    #         if status is not True:
    #             return (False, reason)
    #         return self._generateClubDetail(info=info)
    #     except Exception as e:
    #         print e
    #         db.session.rollback()
    #         errorInfo = ErrorInfo['WOLFS_01']
    #         errorInfo['detail'] = str(e)
    #         return (False, errorInfo)
    #
    # # 获取俱乐部详情
    # def getClubDetail(self, jsonInfo):
    #     info = json.loads(jsonInfo)
    #     try:
    #         # 身份校验
    #         tokenManager = TokenManager()
    #         (status, userID) = tokenManager.isTokenValid(info=info)
    #         if status is not True:
    #             return (False, userID)
    #         return self._generateClubDetail(info=info)
    #     except Exception as e:
    #         print e
    #         db.session.rollback()
    #         errorInfo = ErrorInfo['WOLFS_01']
    #         errorInfo['detail'] = str(e)
    #         return (False, errorInfo)
    #
    #
    # def _generateClubDetail(self, info):
    #     clubID = info['clubID']
    #     query = db.session.query(Club, UserInfo, Province, City, County).outerjoin(
    #         UserInfo, Club.userID == UserInfo.userID
    #     ).outerjoin(
    #         Province, Club.provinceID == Province.provinceID
    #     ).outerjoin(
    #         City, Club.cityID == City.cityID
    #     ).outerjoin(
    #         County, Club.countyID == County.countyID
    #     ).filter(Club.clubID == clubID)
    #     result = query.first()
    #     if result is None:
    #         errorInfo = ErrorInfo['WOLFS_08']
    #         return (False, errorInfo)
    #     callBackData = {}
    #     if result.UserInfo is not None:
    #         (status, userInfo) = UserInfo.generate(result=result.UserInfo)
    #         callBackData.update(userInfo)
    #     (status, provinceInfo) = Province.generate(result=result.Province)
    #     (status, cityInfo) = City.generate(result=result.City)
    #     (status, countyInfo) = County.generate(result=result.County)
    #     (status, clubInfo) = Club.generate(result=result.Club)
    #     callBackData.update(provinceInfo)
    #     callBackData.update(cityInfo)
    #     callBackData.update(countyInfo)
    #     callBackData.update(clubInfo)
    #     imageManager = ImageManager()
    #     info['foreignID'] = clubID
    #     (status, imgInfo) = imageManager.getImage(info=info)
    #     callBackData.update(imgInfo)
    #     return (True, callBackData)
    #
    #
    # # 后台，　删除俱乐部
    # def deleteClubBackground(self, jsonInfo):
    #     info = json.loads(jsonInfo)
    #     clubID = info['clubID']
    #     try:
    #         # 管理员身份校验
    #         adminManager = AdminManager()
    #         (status, reason) = adminManager.adminAuth(jsonInfo)
    #         if status is not True:
    #             return (False, reason)
    #         imageManager = ImageManager()
    #         # 1.删除关联活动
    #         activityQuery = db.session.query(Activity).filter(
    #             Activity.clubID == clubID
    #         )
    #         activityResult = activityQuery.all()
    #         if activityResult is not None:
    #             for i in activityResult:
    #                 db.session.query(Participate).filter(
    #                     Participate.activityID == i.activityID
    #                 ).delete(synchronize_session=False)
    #                 info['foreignID'] = i.activityID
    #                 imageManager.deleteImage(info=info)
    #         activityQuery.delete(synchronize_session=False)
    #         # 2.删除搜索记录
    #         searchKeyQuery = db.session.query(SearchKey).filter(
    #             SearchKey.foreignID == clubID
    #         )
    #         searchKeyQuery.delete(synchronize_session=False)
    #         # 3.删除图像
    #         imgPathQuery = db.session.query(ImgPath).filter(
    #             ImgPath.foreignID == clubID
    #         )
    #         imgPathQuery.delete(synchronize_session=False)
    #         info['foreignID'] = clubID
    #         imageManager.deleteImage(info=info)
    #         #4.删除关联俱乐部
    #         clubQuery = db.session.query(Club).filter(
    #             Club.clubID == clubID
    #         )
    #         clubQuery.delete(synchronize_session=False)
    #         db.session.commit()
    #         return (True, None)
    #     except Exception as e:
    #         print e
    #         db.session.rollback()
    #         errorInfo = ErrorInfo['WOLFS_01']
    #         errorInfo['detail'] = str(e)
    #         return (False, errorInfo)
    #
    # # 获取个人中心中的俱乐部列表
    # @TokenManager.checkUserValidity
    # def getClubListByUserID(self, jsonInfo, **kwargs):
    #     info = kwargs
    #     try:
    #         userID = info['userID']
    #         startIndex = info['startIndex']
    #         pageCount= info['pageCount']
    #         query = db.session.query(ClubScore, Club).outerjoin(
    #             Club, ClubScore.clubID == Club.clubID
    #         ).filter(
    #             and_(ClubScore.userID == userID,
    #                  ClubScore.clubID != '-1')
    #         )
    #         allResult = query.offset(startIndex).limit(pageCount).all()
    #         imageManager = ImageManager()
    #         def generateClubInfo(result):
    #             res = {}
    #             (status, clubInfo) = Club.generate(result=result.Club)
    #             info['foreignID'] = result.Club.clubID
    #             info['directory'] = 'portrait'
    #             (status, imgInfo) = imageManager.getImage(info=info)
    #             res.update(imgInfo)
    #             res.update(clubInfo)
    #             return res
    #         callBackData = [generateClubInfo(result=result) for result in allResult]
    #         return (True, callBackData)
    #     except Exception as e:
    #         print e
    #         db.session.rollback()
    #         errorInfo = ErrorInfo['WOLFS_01']
    #         errorInfo['detail'] = str(e)
    #         return (False, errorInfo)
    #
    # @TokenManager.checkUserValidity
    # def getClubList(self, jsonInfo, **kwargs):
    #     info = kwargs
    #     try:
    #         query = db.session.query(Club)
    #         allResult = query.all()
    #         callBackData = [Club.generate(result=result)[1] for result in allResult]
    #         return (True, callBackData)
    #     except Exception as e:
    #         print e
    #         db.session.rollback()
    #         errorInfo = ErrorInfo['WOLFS_01']
    #         errorInfo['detail'] = str(e)
    #         return (False, errorInfo)