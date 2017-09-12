import sys
sys.path.append("..")
from datetime import datetime
import json
import random
import numpy
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import func
from sqlalchemy import desc

from tool.util import Util
from tool.error_config import ErrorInfo
from stoken.token_manager import TokenManager
from image.image_manager import ImageManager
from model.flaskapp import db
from model.userinfo import UserInfo
from model.token import Token
from model.imgpath import ImgPath
from model.participate import Participate
from model.activity import Activity
from model.club import Club
from model.clubscroe import ClubScore

from tool.config import VALIDITY
from tool.config import ACTIVITY_CLUB
from tool.config import ACTIVITY_USER
from tool.config import ACTIVITY_CREATE_STATE
from tool.config import ACTIVITY_ENTER_FULL_STATE
from tool.config import EMPTY_LOCATION
from tool.config import ROLE_JUDGE
from tool.config import ROLE_EMPTY
from tool.config import EMPTY_LOCATION
from tool.config import ACTIVITY_STATE_START


class ActivityManager(Util):

    def __init__(self):
        super().__init__()

    @TokenManager.check_admin_validity
    @Util.error_print
    def create_activity_background(self, info):
        '''
        后台，创建活动
        第一步: 验证管理员身份
        第二步: 创建Imgpath, Activity信息
        :param info: {'token_id': '', 'user_name': '', 'imgpath': '', 'user_id': '', 'open_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        print(info)
        info['activity_id'] = self.generate_id(info['activity_name'])
        info['imgpath_id'] = self.generate_id(info['imgpath'])
        info['foreign_id'] = info['activity_id']
        ImgPath.create(info=info)
        info['createtime'] = datetime.now()
        if 'club_id' in info:
            info['type_id'] = ACTIVITY_CLUB
            info['area'] = None
        else:
            info['club_id'] = None
            info['type_id'] = ACTIVITY_USER
        Activity.create(info=info)
        db.session.commit()
        return (True, info['activity_id'])

    @TokenManager.check_user_validity
    @Util.error_print
    def create_activity(self, info):
        '''
        创建活动
        第一步: 验证用户身份
        第二步: 创建Imgpath, Activity信息
        :param info: {'token_id': '', 'user_name': '', 'imgpath': '', 'user_id': '', 'open_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        print(info)
        info['activity_id'] = self.generate_id(info['activity_name'])
        info['imgpath_id'] = self.generate_id(info['imgpath'])
        info['foreign_id'] = info['activity_id']
        ImgPath.create(info=info)
        info['createtime'] = datetime.now()
        Activity.create(info=info)
        db.session.commit()
        return (True, info['activity_id'])

    @TokenManager.check_user_validity
    @Util.error_print
    def edit_activity(self, info):
        '''
        编辑活动
        第一步: 验证用户身份
        第二步: 变更活动信息
        :param info: {'token_id': '', 'user_name': '', 'imgpath': '', 'user_id': '', 'open_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        if result.activity_state < ACTIVITY_STATE_START:
            result.activity_number = info['activity_number']
            result.activity_name = info['activity_name']
            result.description = info['description']
            result.startdate = info['startdate']
            if result.type_id == ACTIVITY_USER:
                result.area = info['area']
            db.session.commit()
            return (True, info['activity_id'])
        else:
            return (False, None)


    @TokenManager.check_user_validity
    @Util.error_print
    def create_participate(self, info):
        '''
        后台，参加活动
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否已经加入,是否已经满员
        第三步: 自动分配活动位置, 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        if not result:
            return (False, ErrorInfo['WOLFS_09'])
        if result.activity_state != ACTIVITY_CREATE_STATE:
            return (False, ErrorInfo['WOLFS_10'])
        part_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.user_id == user_id))
        part_result = part_query.first()
        if part_result:
            return (False, ErrorInfo['WOLFS_11'])
        count_query = db.session.query(func.count(Participate.participate_id)).filter(
            Participate.activity_id == activity_id
        )
        count_number = count_query.first()[0]
        activity_number = result.activity_number
        if count_number > activity_number:
            return (False, ErrorInfo['WOLFS_16'])
        info['createtime'] = datetime.now()
        info['participate_id'] = self.generate_id(user_id + activity_id)
        info['roletype_id'] = ROLE_EMPTY
        info['location'] = EMPTY_LOCATION
        Participate.create(info=info)
        db.session.commit()
        return (True, info['participate_id'])

    def _generate_location(self, info):
        '''
        生成活动位置
        第一种情况: 报名人数小于活动规定最小值, 随机一个位置(不大于最小值)
        第二种情况: 报名人数大于最小值,但是小于最大值, 位置设置为当前人数加上1
                   同时,将活动状态修改为不可以报名
        :param info: 
        :return: 
        '''
        activity_id = info['activity_id']
        min_number = info['min_number']
        max_number = info['max_number']
        query = db.session.query(Participate.location).filter(
            Participate.activity_id == activity_id
        )
        all_result = query.all()
        current_number = len(all_result)
        if current_number < min_number:
            choice_list = numpy.setdiff1d(list(range(1, min_number + 1)), list(all_result))
            location = random.choice(choice_list)
        else:
            location = current_number + 1
            if location == max_number:
                activity_query = info['activity_query']
                update_info = {Activity.activity_state: ACTIVITY_ENTER_FULL_STATE}
                activity_query.update(update_info, synchronize_session=False)
        return (True, location)

    @TokenManager.check_user_validity
    @Util.error_print
    def get_activity_list(self, info):
        '''
        活动列表
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否已经加入,是否已经满员
        第三步: 自动分配活动位置, 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        type_id = info['type_id']
        start_index = info['start_index']
        page_count = info['page_count']
        query = db.session.query(Activity).filter(and_(
            Activity.type_id == type_id, Activity.activity_state < ACTIVITY_STATE_START)
        )
        all_result = query.order_by(desc(Activity.createtime)).offset(start_index).limit(page_count).all()
        callback_data = []
        img_request = {}
        img_request['directory'] = 'activity'
        imagemanager = ImageManager()
        for result in all_result:
            (status, activity_info) = Activity.generate(result=result)
            img_request['foreign_id'] = result.activity_id
            (status, image_info) = imagemanager.get_image(info=img_request)
            activity_info.update(image_info)
            callback_data.append(activity_info)
        return (True, callback_data)

    @TokenManager.check_user_validity
    @Util.error_print
    def get_create_activity_list(self, info):
        '''
        我创建的活动列表
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否已经加入,是否已经满员
        第三步: 自动分配活动位置, 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        start_index = info['start_index']
        page_count = info['page_count']
        user_id = info['user_id']
        query = db.session.query(Activity).filter(Activity.user_id == user_id)
        all_result = query.order_by(desc(Activity.createtime)).offset(start_index).limit(page_count).all()
        callback_data = []
        img_request = {}
        img_request['directory'] = 'activity'
        imagemanager = ImageManager()
        for result in all_result:
            (status, activity_info) = Activity.generate(result=result)
            img_request['foreign_id'] = result.activity_id
            (status, image_info) = imagemanager.get_image(info=img_request)
            activity_info.update(image_info)
            callback_data.append(activity_info)
        return (True, callback_data)

    @TokenManager.check_user_validity
    @Util.error_print
    def get_participate_activity_list(self, info):
        '''
        我参加的活动列表
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否已经加入,是否已经满员
        第三步: 自动分配活动位置, 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        start_index = info['start_index']
        page_count = info['page_count']
        user_id = info['user_id']
        query = db.session.query(Participate, Activity).outerjoin(
            Activity, Participate.activity_id == Activity.activity_id
        ).filter(Participate.user_id == user_id)
        all_result = query.order_by(desc(Activity.createtime)).offset(start_index).limit(page_count).all()
        callback_data = []
        img_request = {}
        img_request['directory'] = 'activity'
        imagemanager = ImageManager()
        for result in all_result:
            (status, activity_info) = result.Activity.generate(result=result.Activity)
            img_request['foreign_id'] = result.Activity.activity_id
            (status, image_info) = imagemanager.get_image(info=img_request)
            activity_info.update(image_info)
            callback_data.append(activity_info)
        return (True, callback_data)

    @TokenManager.check_user_validity
    @Util.error_print
    def get_participate_club_list(self, info):
        '''
        我参加的俱乐部列表
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否已经加入,是否已经满员
        第三步: 自动分配活动位置, 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        user_id = info['user_id']
        query = db.session.query(Participate, Activity).outerjoin(
            Activity, Participate.activity_id == Activity.activity_id
        ).filter(and_(Participate.user_id == user_id,
                      Activity.type_id == ACTIVITY_CLUB))
        all_result = query.order_by(desc(Activity.createtime)).all()
        club_id_tuple = (result.Activity.club_id for result in all_result)
        club_query = db.session.query(Club).filter(Club.club_id.in_(club_id_tuple))
        all_club_result = club_query.all()
        callback_data = []
        img_request = {}
        img_request['directory'] = 'club'
        imagemanager = ImageManager()
        for club_result in all_club_result:
            (status, club_info) = club_result.generate(result=club_result)
            img_request['foreign_id'] = club_result.club_id
            (status, image_info) = imagemanager.get_image(info=img_request)
            club_info.update(image_info)
            callback_data.append(club_info)
        return (True, callback_data)

    @TokenManager.check_user_validity
    @Util.error_print
    def get_club_list(self, info):
        '''
        活动列表
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否已经加入,是否已经满员
        第三步: 自动分配活动位置, 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        query = db.session.query(Club)
        all_result = query.order_by(desc(Club.createtime)).all()
        callback_data = []
        for result in all_result:
            (status, club_info) = Club.generate(result=result)
            callback_data.append(club_info)
        return (True, callback_data)

    @TokenManager.check_user_validity
    @Util.error_print
    def get_room_detail(self, info):
        '''
        活动详情
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否已经加入,是否已经满员
        第三步: 自动分配活动位置, 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        (status, activity_detail) = self._get_activity_detail(info)
        (status, judge_info) = self._get_activity_judge(info)
        part_query = db.session.query(Participate, UserInfo).outerjoin(
            UserInfo, Participate.user_id == UserInfo.user_id
        ).filter(Participate.activity_id == activity_id)
        all_result = part_query.order_by(Participate.location).all()
        role_list = []
        callback_data = {}
        my_info = {}
        img_request = {}
        imagemanager = ImageManager()
        for result in all_result:
            participate = result.Participate
            user = result.UserInfo
            img_request['foreign_id'] = participate.user_id
            (status, part_info) = Participate.generate(result=participate)
            if user.open_id is None:
                (status, image_info) = imagemanager.get_image(info=img_request)
            else:
                imgpath = db.session.query(ImgPath).filter(ImgPath.foreign_id == user.user_id).first()
                (status, image_info) = ImgPath.generate(result=imgpath)
            (status, user_info) = UserInfo.generate(result=user)
            part_info.update(image_info)
            part_info.update(user_info)
            if part_info['user_id'] == user_id:
                my_info.update(part_info)
            role_list.append(part_info)
        callback_data['role_list'] = role_list
        callback_data['activity_detail'] = activity_detail
        callback_data['judge_info'] = judge_info
        callback_data['my_info'] = my_info
        return (True, callback_data)

    def _get_activity_detail(self, info):
        activity_id = info['activity_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        img_request = {}
        img_request['directory'] = 'activity'
        img_request['foreign_id'] = activity_id
        imagemanager = ImageManager()
        (status, activity_info) = Activity.generate(result=result)
        (status, image_info) = imagemanager.get_image(info=img_request)
        activity_info.update(image_info)
        return (True, activity_info)

    def _get_activity_judge(self, info):
        judge_info = {}
        judge_exist = False
        judge_state = False
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == ROLE_JUDGE))
        result = query.first()
        if result:
            judge_exist = True
            imgpath = db.session.query(ImgPath).filter(ImgPath.foreign_id == result.user_id).first()
            (status, image_info) = ImgPath.generate(result=imgpath)
            judge_info['imgpath'] = image_info['imgpath']
        judge_result = query.filter(Participate.user_id == user_id).first()
        if judge_result:
            judge_state = True
        judge_info['judge_exist'] = judge_exist
        judge_info['judge_state'] = judge_state

        return (True, judge_info)

    @TokenManager.check_user_validity
    @Util.error_print
    def assign_location(self, info):
        '''
        变更用户位置
        第一步: 验证用户身份
        第二步: 判断现在的位置是否处于未分配状态
        第三步: 变更位置
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        location = info['location']
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Participate).filter(
            and_(
                Participate.activity_id == activity_id,
                Participate.user_id == user_id,
                Participate.location == EMPTY_LOCATION
            ))
        result = query.first()
        if not result:
            return (False, None)
        query.update({Participate.location: location}, synchronize_session=False)
        db.session.commit()
        return (True, None)

    @TokenManager.check_user_validity
    @Util.error_print
    def user_leave_seat(self, info):
        '''
        用户离座
        第一步: 验证用户身份
        第二步: 变更用户位置，身份信息，从用户身份变成未分配身份，从用户位置变成未分配位置
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Participate).filter(
            and_(
                Participate.activity_id == activity_id,
                Participate.user_id == user_id
            )
        )
        query.update({Participate.roletype_id: ROLE_EMPTY,
                      Participate.location: EMPTY_LOCATION},
                      synchronize_session=False)
        db.session.commit()
        return (True, None)


    @TokenManager.check_user_validity
    @Util.error_print
    def get_score_list(self, info):
        '''
        积分列表
        第一步: 验证用户身份
        第二步: 获取积分列表
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        user_id = info['user_id']
        start_index = info['start_index']
        page_count = info['page_count']
        query = db.session.query(UserInfo)
        all_result = query.order_by(desc(UserInfo.user_score)).offset(start_index).limit(page_count).all()
        callback_data = []
        imagemanager = ImageManager()
        img_request = {}
        for result in all_result:
            (status, user_info) = UserInfo.generate(result=result)
            count = db.session.query(
                func.count(UserInfo.user_id)
            ).filter(
                UserInfo.user_score > user_info['user_score']
            ).first()
            user_info['index_number'] = count[0] + 1
            img_request['foreign_id'] = result.user_id
            if result.open_id is None:
                (status, image_info) = imagemanager.get_image(info=img_request)
            else:
                imgpath = db.session.query(ImgPath).filter(ImgPath.foreign_id == result.user_id).first()
                (status, image_info) = ImgPath.generate(result=imgpath)
            user_info.update(image_info)
            callback_data.append(user_info)
        return (True, callback_data)

    @TokenManager.check_user_validity
    # @Util.error_print
    def get_club_score_list(self, info):
        '''
        俱乐部积分列表
        第一步: 验证用户身份
        第二步: 获取积分最多的俱乐部积分列表
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        user_id = info['user_id']
        start_index = info['start_index']
        page_count = info['page_count']
        if info['club_id'] == '-1':
            club_query = db.session.query(ClubScore).filter(ClubScore.user_id == user_id)
            club_result = club_query.order_by(desc(ClubScore.club_number)).first()
        else:
            club_result = db.session.query(ClubScore).filter(ClubScore.club_id == info['club_id']).first()
            print(club_result)
        if club_result:
            club_id = club_result.club_id
            query = db.session.query(UserInfo, ClubScore).outerjoin(
                ClubScore, UserInfo.user_id == ClubScore.user_id
            ).filter(ClubScore.club_id == club_id)
            all_result = query.order_by(desc(ClubScore.club_number)).offset(start_index).limit(page_count).all()
            callback_data = []
            imagemanager = ImageManager()
            img_request = {}
            for result in all_result:
                user = result.UserInfo
                clubscore = result.ClubScore
                (status, _club) = ClubScore.generate(result=clubscore)
                (status, _user_info) = UserInfo.generate(result=user)
                count = db.session.query(
                    func.count(ClubScore.score_id)
                ).filter(
                    and_(
                        ClubScore.club_id == club_id,
                        ClubScore.club_number > _club['club_number']
                    )
                ).first()
                _club['index_number'] = count[0] + 1
                img_request['foreign_id'] = user.user_id
                if user.open_id is None:
                    (status, image_info) = imagemanager.get_image(info=img_request)
                else:
                    imgpath = db.session.query(ImgPath).filter(ImgPath.foreign_id == user.user_id).first()
                    (status, image_info) = ImgPath.generate(result=imgpath)
                _club.update(image_info)
                _club.update(_user_info)
                callback_data.append(_club)
            return (True, callback_data)
        else:
            return (False, None)


if __name__ == '__main__':
    pass