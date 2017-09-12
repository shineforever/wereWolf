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
from model.operate import Operate
from model.clubscroe import ClubScore

from tool.config import ROLE_JUDGE
from tool.config import ROLE_WEREWOLF
from tool.config import ROLE_EMPTY
from tool.config import ACTIVITY_CLUB
from tool.config import SCORE_VILLAGER
from tool.config import SCORE_WEREWOLF
from tool.config import SCORE_EMPTY
from tool.config import OPERATE_ASSIGN_ROLE
from tool.config import OPERATE_START_ACTIVITY
from tool.config import OPERATE_PARTICIPANT_OUT
from tool.config import ACTIVITY_STATE_START
from tool.config import ACTIVITY_CREATE_STATE
from tool.config import ACTIVITY_STATE_END
from tool.config import ACTIVITY_STATE_SCORE
from tool.config import EMPTY_LOCATION




class JudgeManager(Util):

    def __init__(self):
        super().__init__()

    @TokenManager.check_user_validity
    @Util.error_print
    def create_judge(self, info):
        '''
        称为法官
        第一步: 验证用户身份
        第二步: 判断活动是否存在，是否存在法官
        第三步: 创建参加记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        if not result:
            return (False, ErrorInfo['WOLFS_09'])
        part_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == ROLE_JUDGE))
        part_result = part_query.first()
        if part_result:
            return (False, ErrorInfo['WOLFS_12'])
        user_query = db.session.query(Participate).filter(
            and_(
                Participate.activity_id == activity_id,
                Participate.user_id == user_id
            )
        )
        user_query.update({Participate.roletype_id: ROLE_JUDGE,
                           Participate.location: EMPTY_LOCATION},
                          synchronize_session=False)
        db.session.commit()
        return (True, None)


    @TokenManager.check_user_validity
    @Util.error_print
    def judge_leave_seat(self, info):
        '''
        法官离座
        第一步: 验证用户身份
        第二步: 变更用户位置，身份信息，从法官身份变成未分配身份，从法官位置变成未分配位置
        第三步: 变更所有活动参加者身份信息为未分配，变更活动状态，删除法官操作历史记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Participate).filter(
            and_(
                Participate.activity_id == activity_id,
                Participate.user_id == user_id,
                Participate.roletype_id == ROLE_JUDGE
            )
        )
        query.update({Participate.roletype_id: ROLE_EMPTY,
                      Participate.location: EMPTY_LOCATION},
                      synchronize_session=False)
        user_query = db.session.query(Participate).filter(
            Participate.activity_id == activity_id
        )
        user_query.update({Participate.roletype_id: ROLE_EMPTY,
                           Participate.score: SCORE_EMPTY,
                           Participate.state: False}, synchronize_session=False)
        activity_query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        activity_query.update({Activity.activity_state: ACTIVITY_CREATE_STATE}, synchronize_session=False)
        operate_query = db.session.query(Operate).filter(and_(Operate.activity_id == activity_id,
                                              Operate.user_id == user_id))
        operate_query.delete(synchronize_session=False)
        db.session.commit()
        return (True, None)

    @TokenManager.check_user_validity
    @Util.error_print
    def assign_role(self, info):
        '''
        称为法官
        第一步: 验证用户身份
        第二步: 判断活动是否存在, 是否是该活动的法官
        第三步: 更新用户在活动中的角色信息
        第四步: 添加法官操作记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        if not result:
            return (False, ErrorInfo['WOLFS_09'])
        part_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == ROLE_JUDGE,
                 Participate.user_id == user_id))
        part_result = part_query.first()
        if not part_result:
            return (False, ErrorInfo['WOLFS_13'])
        roletype_id = info['roletype_id']
        foreign_id_list = info['foreign_id_list']
        role_query = db.session.query(Participate).filter(Participate.user_id.in_(foreign_id_list))
        role_query.update({Participate.roletype_id: roletype_id}, synchronize_session=False)
        info['type_id'] = OPERATE_ASSIGN_ROLE
        (status, _) = self._create_operate(info=info)
        db.session.commit()
        return (True, None)

    def _create_operate(self, info):
        operate_info = {}
        operate_info['activity_id'] = info['activity_id']
        operate_info['createtime'] = datetime.now()
        operate_info['user_id'] = info['user_id']
        operate_info['type_id'] = info['type_id']
        foreign_id_list = info['foreign_id_list']
        query = db.session.query(Operate).filter(and_(
            Operate.user_id == operate_info['user_id'],
            Operate.activity_id == operate_info['activity_id']
        ))
        result = query.order_by(desc(Operate.level_number)).first()
        if not result:
            operate_info['level_number'] = 1
        else:
            operate_info['level_number'] = result.level_number + 1
        for foreign_id in foreign_id_list:
            operate_info['foreign_id'] = foreign_id
            operate_info['operate_id'] = self.generate_id(operate_info['user_id'])
            Operate.create(info=operate_info)
        return (True, None)

    @TokenManager.check_user_validity
    @Util.error_print
    def revoke_operate(self, info):
        '''
        撤销操作
        第一步: 验证用户身份，判断活动是否存在, 是否是该活动的法官
        第二步：根据操作记录，选择合适的撤销函数，执行
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        if not result:
            return (False, ErrorInfo['WOLFS_09'])
        part_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == ROLE_JUDGE,
                 Participate.user_id == user_id))
        part_result = part_query.first()
        if not part_result:
            return (False, ErrorInfo['WOLFS_13'])
        func_list = {'1': self._revoke_assign_role_operate, '2': self._revoke_start_acvitity,
                     '3': self._revoke_paticipatant_out}
        query = db.session.query(Operate).filter(and_(Operate.user_id == user_id,
                                              Operate.activity_id == activity_id))
        result = query.order_by(desc(Operate.level_number)).first()
        if not result:
            return (False, None)
        type_id = result.type_id
        info['level_number'] = result.level_number
        (status, _) = func_list[type_id](info=info)
        db.session.commit()
        return (True, None)

    def _revoke_assign_role_operate(self, info):
        '''
        撤销分配角色操作
        :param info: 
        :return: 
        '''
        level_number = info['level_number']
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Operate).filter(
            and_(Operate.user_id == user_id,
                 Operate.activity_id == activity_id,
                 Operate.level_number == level_number))
        all_result = query.all()
        foreign_id_tuple = (result.foreign_id for result in all_result)
        part_query = db.session.query(Participate).filter(
            and_(
                Participate.activity_id == activity_id,
                Participate.user_id.in_(foreign_id_tuple)
            ))
        part_query.update({Participate.roletype_id: ROLE_EMPTY}, synchronize_session=False)
        query.delete(synchronize_session=False)
        return (True, None)

    def _revoke_start_acvitity(self, info):
        '''
        撤销开始活动操作
        :param info: 
        :return: 
        '''
        level_number = info['level_number']
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Operate).filter(
            and_(Operate.user_id == user_id,
                 Operate.activity_id == activity_id,
                 Operate.level_number == level_number))
        result = query.first()
        activity_state = int(result.foreign_id)
        activity_query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        activity_query.update({Activity.activity_state: activity_state}, synchronize_session=False)
        query.delete(synchronize_session=False)
        return (True, None)

    def _revoke_paticipatant_out(self, info):
        '''
        撤销玩家出局操作
        第一步：判断出局人员是否是某一方的最后一个出局者，
            　　如果是，需要变更整个活动中人员的积分，否则只需要变更出局者的状态
        第二步：变更活动中人员积分，个人总的积分
        第三步：变更出局者的状态，删除操作记录
        :param info: 
        :return: 
        '''
        level_number = info['level_number']
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Operate).filter(
            and_(Operate.user_id == user_id,
                 Operate.activity_id == activity_id,
                 Operate.level_number == level_number))
        result = query.first()
        foreign_id = result.foreign_id
        part_query = db.session.query(Participate).filter(
            and_(
                Participate.activity_id == activity_id,
                Participate.user_id == foreign_id
        ))
        part_result = part_query.first()
        score = part_result.score
        roletype_id = part_result.roletype_id
        if score != 0:
            user_query = db.session.query(Participate, UserInfo).outerjoin(
                UserInfo, Participate.user_id == UserInfo.user_id
            ).filter(
                Participate.activity_id == activity_id
            )
            all_result = user_query.all()
            if roletype_id == ROLE_WEREWOLF:
                for result in all_result:
                    participate = result.Participate
                    userinfo = result.UserInfo
                    score = -SCORE_WEREWOLF[participate.roletype_id]
                    participate.score = 0
                    userinfo.score = -score + userinfo.score
            else:
                for result in all_result:
                    participate = result.Participate
                    userinfo = result.UserInfo
                    score = SCORE_VILLAGER[participate.roletype_id]
                    participate.score = 0
                    userinfo.score = -score + userinfo.score
        part_query.update({Participate.state: False}, synchronize_session=False)
        query.delete(synchronize_session=False)
        return (True, None)

    @TokenManager.check_user_validity
    @Util.error_print
    def start_activity(self, info):
        '''
        开始活动
        第一步: 验证用户身份,判断活动是否存在, 是否是该活动的法官
        第二步: 检查参加活动者是否都已经分配角色
        第四步: 添加法官操作记录，开始活动
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        if not result:
            return (False, ErrorInfo['WOLFS_09'])
        judge_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == ROLE_JUDGE,
                 Participate.user_id == user_id))
        judge_result = judge_query.first()
        if not judge_result:
            return (False, ErrorInfo['WOLFS_13'])
        part_query = db.session.query(Participate).filter(
            and_(Participate.location != None,
                 Participate.roletype_id == None,
                 Participate.activity_id == activity_id)
        )
        part_result = part_query.all()
        if part_result:
            return (False, ErrorInfo['WOLFS_14'])
        info['type_id'] = OPERATE_START_ACTIVITY
        info['foreign_id_list'] = [str(result.activity_state), ]
        (status, _) = self._create_operate(info=info)
        query.update({Activity.activity_state: ACTIVITY_STATE_START}, synchronize_session=False)
        db.session.commit()
        return (True, None)

    @TokenManager.check_user_validity
    @Util.error_print
    def end_activity(self, info):
        '''
        开始活动
        第一步: 验证用户身份,判断活动是否存在, 是否是该活动的法官
        第二步: 判断活动是否已经结束，
        第三步：改变活动状态为结束状态，删除法官操作记录,
        第四步：如果是俱乐部活动，　改变玩家俱乐部积分
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        query = db.session.query(Activity).filter(
            Activity.activity_id == activity_id
        )
        result = query.first()
        if not result:
            return (False, ErrorInfo['WOLFS_09'])
        judge_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == ROLE_JUDGE,
                 Participate.user_id == user_id))
        judge_result = judge_query.first()
        if not judge_result:
            return (False, ErrorInfo['WOLFS_13'])
        if result.activity_state != ACTIVITY_STATE_SCORE:
            return (False, ErrorInfo['WOLFS_15'])
        query.update(
            {Activity.activity_state: ACTIVITY_STATE_END},
            synchronize_session=False
        )
        operate_query = db.session.query(Operate).filter(
            Operate.activity_id == activity_id
        )
        operate_query.delete(synchronize_session=False)
        if result.type_id == ACTIVITY_CLUB:
            club_id = result.club_id
            part_query = db.session.query(Participate).filter(
                Participate.activity_id == activity_id
            )
            all_result = part_query.all()
            for part_result in all_result:
                club_query = db.session.query(ClubScore).filter(
                    and_(ClubScore.user_id == part_result.user_id,
                         ClubScore.club_id == club_id)
                )
                club_result = club_query.first()
                if not club_result:
                    club_score_info = {}
                    club_score_info['score_id'] = self.generate_id(part_result.user_id + club_id)
                    club_score_info['user_id'] = part_result.user_id
                    club_score_info['club_number'] = part_result.score
                    club_score_info['club_id'] = club_id
                    ClubScore.create(info=club_score_info)
                else:
                    club_query.update(
                        {ClubScore.club_number: ClubScore.club_number + part_result.score},
                        synchronize_session=False
                    )
        db.session.commit()
        return (True, None)

    @TokenManager.check_user_validity
    @Util.error_print
    def get_score_info(self, info):
        '''
        获取活动成绩
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        part_query = db.session.query(Participate, UserInfo).outerjoin(
            UserInfo, Participate.user_id == UserInfo.user_id
        ).filter(and_(Participate.activity_id == activity_id, Participate.score != SCORE_EMPTY))
        all_result = part_query.order_by(desc(Participate.score)).all()
        callback_data = []
        img_request = {}
        imagemanager = ImageManager()
        for score_result in all_result:
            user = score_result.UserInfo
            participate = score_result.Participate
            img_request['foreign_id'] = participate.user_id
            if user.open_id is None:
                (status, image_info) = imagemanager.get_image(info=img_request)
            else:
                imgpath = db.session.query(ImgPath).filter(ImgPath.foreign_id == user.user_id).first()
                (status, image_info) = ImgPath.generate(result=imgpath)
            (status, part_info) = Participate.generate(result=participate)
            (status, user_info) = UserInfo.generate(result=user)
            part_info.update(user_info)
            part_info.update(image_info)
            callback_data.append(part_info)
        return (True, callback_data)

    @TokenManager.check_user_validity
    @Util.error_print
    def participant_out(self, info):
        '''
        玩家出局
        第一步: 验证用户身份,判断活动是否存在, 是否是该活动的法官
        第二步: 添加法官操作记录
        :param info: {'token_id': '', 'user_id': '', 'activity_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        activity_id = info['activity_id']
        user_id = info['user_id']
        foreign_id = info['foreign_id']
        query = db.session.query(Activity).filter(Activity.activity_id == activity_id)
        result = query.first()
        if not result:
            return (False, ErrorInfo['WOLFS_09'])
        judge_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == ROLE_JUDGE,
                 Participate.user_id == user_id))
        judge_result = judge_query.first()
        if not judge_result:
            return (False, ErrorInfo['WOLFS_13'])
        part_query = db.session.query(Participate).filter(
            and_(
                Participate.activity_id == activity_id,
                Participate.user_id == foreign_id
            )
        )
        part_result = part_query.first()
        info['roletype_id'] = part_result.roletype_id
        info['type_id'] = OPERATE_PARTICIPANT_OUT
        info['foreign_id_list'] = [foreign_id, ]
        (status, _) = self._create_operate(info=info)
        (score_status, _) = self._auto_score(info=info)
        if score_status:
            query.update({Activity.activity_state: ACTIVITY_STATE_SCORE},synchronize_session=False)
        part_query.update({Participate.state: True}, synchronize_session=False)
        db.session.commit()
        return (True, None)

    def _auto_score(self, info):
        '''
        自动计算积分
        第一步：判断是否有一方全部被出局，如果有，积分变更，执行第二步，否则，直接返回
        第二步： 变更活动中人员积分，个人总的积分
        :param info: 
        :return: 
        '''
        activity_id = info['activity_id']
        roletype_id = info['roletype_id']
        role_query = db.session.query(Participate).filter(
            and_(Participate.activity_id == activity_id,
                 Participate.roletype_id == roletype_id,
                 Participate.state == False)
        )
        role_result = role_query.all()
        if len(role_result) == 1:
            query = db.session.query(Participate, UserInfo).outerjoin(
                UserInfo, Participate.user_id == UserInfo.user_id
            ).filter(
                Participate.activity_id == activity_id
            )
            all_result = query.all()
            if roletype_id == ROLE_WEREWOLF:
                for result in all_result:
                    participate = result.Participate
                    userinfo = result.UserInfo
                    score = SCORE_WEREWOLF[participate.roletype_id]
                    participate.score = score
                    userinfo.user_score = score + userinfo.user_score
            else:
                for result in all_result:
                    participate = result.Participate
                    userinfo = result.UserInfo
                    score = SCORE_VILLAGER[participate.roletype_id]
                    participate.score = score
                    userinfo.user_score = score + userinfo.user_score
            return (True, None)
        else:
            return (False, None)

if __name__ == '__main__':
    pass
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()