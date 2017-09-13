import sys
sys.path.append('..')
import json
from flask import request
from user.admin_manager import AdminManager
from club.club_manager import ClubManager
from user.user_manager import UserManager
from activity.activity_manager import ActivityManager
from judge.judge_manager import JudgeManager
from image.image_manager import ImageManager
from model.flaskapp import app



#通用返回接口
def generate_call_back(method):
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        paramsJson = request.form['data']
        (status, jsonlist) = method(paramsJson)
        if status is not False:
            data['status'] = 'SUCCESS'
        data['data'] = jsonlist
        return json.dumps(data)

#===================用户管理====================================
# 后台，　创建后台管理员
@app.route('/create_admin_info_background/', methods=['POST', 'GET'])
def create_admin_info_background():
    adminmanager = AdminManager()
    method = adminmanager.create_admin_info_background
    return generate_call_back(method=method)

# 后台，　管理员登录
@app.route('/admin_login_background/', methods=['POST', 'GET'])
def admin_login_background():
    adminmanager = AdminManager()
    method = adminmanager.admin_login_background
    return generate_call_back(method=method)

#后台，创建用户
@app.route('/create_user_background/', methods=['POST', 'GET'])
def create_user_background():
    usermanager = UserManager()
    method = usermanager.create_user_background
    return generate_call_back(method=method)

#微信小程序用户登录
@app.route('/wechat_login/', methods=['POST', 'GET'])
def wechat_login():
    usermanager = UserManager()
    method = usermanager.wechat_login
    return generate_call_back(method=method)

#===================活动管理====================================
#后台， 创建活动
@app.route('/create_activity_background/', methods=['POST', 'GET'])
def create_activity_background():
    activitymanager = ActivityManager()
    method = activitymanager.create_activity_background
    return generate_call_back(method=method)

#创建活动
@app.route('/create_activity/', methods=['POST', 'GET'])
def create_activity():
    activitymanager = ActivityManager()
    method = activitymanager.create_activity
    return generate_call_back(method=method)

#编辑活动
@app.route('/edit_activity/', methods=['POST', 'GET'])
def edit_activity():
    activitymanager = ActivityManager()
    method = activitymanager.edit_activity
    return generate_call_back(method=method)

#参加活动
@app.route('/create_participate/', methods=['POST', 'GET'])
def create_participate():
    activitymanager = ActivityManager()
    method = activitymanager.create_participate
    return generate_call_back(method=method)

#活动列表
@app.route('/get_activity_list/', methods=['POST', 'GET'])
def get_activity_list():
    activitymanager = ActivityManager()
    method = activitymanager.get_activity_list
    return generate_call_back(method=method)

#创建的活动列表
@app.route('/get_create_activity_list/', methods=['POST', 'GET'])
def get_create_activity_list():
    activitymanager = ActivityManager()
    method = activitymanager.get_create_activity_list
    return generate_call_back(method=method)

#参加的活动列表
@app.route('/get_participate_activity_list/', methods=['POST', 'GET'])
def get_participate_activity_list():
    activitymanager = ActivityManager()
    method = activitymanager.get_participate_activity_list
    return generate_call_back(method=method)

#参加的俱乐部列表
@app.route('/get_participate_club_list/', methods=['POST', 'GET'])
def get_participate_club_list():
    activitymanager = ActivityManager()
    method = activitymanager.get_participate_club_list
    return generate_call_back(method=method)

#俱乐部列表
@app.route('/get_club_list/', methods=['POST', 'GET'])
def get_club_list():
    activitymanager = ActivityManager()
    method = activitymanager.get_club_list
    return generate_call_back(method=method)


#房间详情
@app.route('/get_room_detail/', methods=['POST', 'GET'])
def get_room_detail():
    activitymanager = ActivityManager()
    method = activitymanager.get_room_detail
    return generate_call_back(method=method)

#变更房间位置
@app.route('/assign_location/', methods=['POST', 'GET'])
def assign_location():
    activitymanager = ActivityManager()
    method = activitymanager.assign_location
    return generate_call_back(method=method)

#用户离座
@app.route('/user_leave_seat/', methods=['POST', 'GET'])
def user_leave_seat():
    activitymanager = ActivityManager()
    method = activitymanager.user_leave_seat
    return generate_call_back(method=method)

#积分列表
@app.route('/get_score_list/', methods=['POST', 'GET'])
def get_score_list():
    activitymanager = ActivityManager()
    method = activitymanager.get_score_list
    return generate_call_back(method=method)

#获取俱乐部积分列表
@app.route('/get_club_score_list/', methods=['POST', 'GET'])
def get_club_score_list():
    activitymanager = ActivityManager()
    method = activitymanager.get_club_score_list
    return generate_call_back(method=method)


#===================法官操作管理====================================
#成为法官
@app.route('/create_judge/', methods=['POST', 'GET'])
def create_judge():
    judgemanager = JudgeManager()
    method = judgemanager.create_judge
    return generate_call_back(method=method)


#法官离座
@app.route('/judge_leave_seat/', methods=['POST', 'GET'])
def judge_leave_seat():
    judgemanager = JudgeManager()
    method = judgemanager.judge_leave_seat
    return generate_call_back(method=method)


#分配角色
@app.route('/assign_role/', methods=['POST', 'GET'])
def assign_role():
    judgemanager = JudgeManager()
    method = judgemanager.assign_role
    return generate_call_back(method=method)

#撤销操作
@app.route('/revoke_operate/', methods=['POST', 'GET'])
def revoke_operate():
    judgemanager = JudgeManager()
    method = judgemanager.revoke_operate
    return generate_call_back(method=method)

#开始活动
@app.route('/start_activity/', methods=['POST', 'GET'])
def start_activity():
    judgemanager = JudgeManager()
    method = judgemanager.start_activity
    return generate_call_back(method=method)

#结束活动
@app.route('/end_activity/', methods=['POST', 'GET'])
def end_activity():
    judgemanager = JudgeManager()
    method = judgemanager.end_activity
    return generate_call_back(method=method)

#获取活动成绩
@app.route('/get_score_info/', methods=['POST', 'GET'])
def get_score_info():
    judgemanager = JudgeManager()
    method = judgemanager.get_score_info
    return generate_call_back(method=method)

#玩家出局
@app.route('/participant_out/', methods=['POST', 'GET'])
def participant_out():
    judgemanager = JudgeManager()
    method = judgemanager.participant_out
    return generate_call_back(method=method)

#上传微信图片到阿里云oss
@app.route('/upload_file/', methods=['POST', 'GET'])
def upload_file():
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    imageManager = ImageManager()
    upload_info = {}
    upload_info['img_file'] = request.files['file']
    upload_info['directory'] = 'activity'
    (status, jsonlist) = imageManager.upload_image(upload_info=upload_info)
    if status is not False:
        data['status'] = 'SUCCESS'
    data['data'] = jsonlist
    return json.dumps(data)


#===================俱乐部管理====================================
#后台， 创建俱乐部
@app.route('/create_club_background/', methods=['POST', 'GET'])
def create_club_background():
    clubManager = ClubManager()
    method = clubManager.create_club_background
    return generate_call_back(method=method)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5098)
