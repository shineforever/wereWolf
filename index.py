import sys
sys.path.append('..')
import json
from flask import request
from user.admin_manager import AdminManager
from club.club_manager import ClubManager
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
    adminManager = AdminManager()
    method = adminManager.create_admin_info_background
    return generate_call_back(method=method)

# 后台，　管理员登录
@app.route('/admin_login_background/', methods=['POST', 'GET'])
def admin_login_background():
    adminManager = AdminManager()
    method = adminManager.admin_login_background
    return generate_call_back(method=method)


#===================俱乐部管理====================================
#后台， 创建俱乐部
@app.route('/create_club_background/', methods=['POST', 'GET'])
def create_club_background():
    clubManager = ClubManager()
    method = clubManager.create_club_background
    return generate_call_back(method=method)
#
# #后台，创建用户
# @app.route('/create_user_background/', methods=['POST', 'GET'])
# def create_user_background():
#     userInfoManager = UserInfoManager()
#     method = userInfoManager.createUserBackground
#     return generate_call_back_with_file(method=method)
#
# #后台，获取用户详情
# @app.route('/get_user_info_detail_background/', methods=['POST', 'GET'])
# def get_user_info_detail_background():
#     userInfoManager = UserInfoManager()
#     method = userInfoManager.getUserInfoDetailBackground
#     return generate_call_back(method=method)
#
#
# #微信小程序，用户注册，登录
# @app.route('/login_with_wechat/', methods=['POST', 'GET'])
# def login_with_wechat():
#     userInfoManager = UserInfoManager()
#     method = userInfoManager.loginWithWechat
#     return generate_call_back(method=method)
#
# #获取用户详情
# @app.route('/get_user_info_detail/', methods=['POST', 'GET'])
# def get_user_info_detail():
#     userInfoManager = UserInfoManager()
#     method = userInfoManager.getUserInfoDetail
#     return generate_call_back(method=method)
#
# #后台, 获取用户列表
# @app.route('/get_user_list_background/', methods=['POST', 'GET'])
# def get_user_list_background():
#     userInfoManager = UserInfoManager()
#     method = userInfoManager.getUserListBackground
#     return generate_call_back(method=method)
#

#
# #后台，　获取俱乐部详情
# @app.route('/get_club_detail_background/', methods=['POST', 'GET'])
# def get_club_detail_background():
#     clubManager = ClubManager()
#     method = clubManager.getClubDetailBackground
#     return generate_call_back(method=method)
#
# #获取俱乐部详情
# @app.route('/get_club_detail/', methods=['POST', 'GET'])
# def get_club_detail():
#     clubManager = ClubManager()
#     method = clubManager.getClubDetail
#     return generate_call_back(method=method)
#
#
# #===================活动管理====================================
# #后台，　创建活动
# @app.route('/create_activity_background/', methods=['POST', 'GET'])
# def create_activity_background():
#     activityManager = ActivityManager()
#     method = activityManager.createActivityBackground
#     return generate_call_back_with_file(method=method)
#
#
# #创建活动
# @app.route('/create_activity/', methods=['POST', 'GET'])
# def create_activity():
#     activityManager = ActivityManager()
#     method = activityManager.createActivity
#     return generate_call_back_with_file(method=method)
#
#
# #后台，　获取活动详情
# @app.route('/get_activity_detail_background/', methods=['POST', 'GET'])
# def get_activity_detail_background():
#     activityManager = ActivityManager()
#     method = activityManager.getActivityDetailBackground
#     return generate_call_back(method=method)
#
# #获取活动详情
# @app.route('/get_activity_detail/', methods=['POST', 'GET'])
# def get_activity_detail():
#     activityManager = ActivityManager()
#     method = activityManager.getActivityDetail
#     return generate_call_back(method=method)
#
# #获取普通活动列表
# @app.route('/get_user_activity_list/', methods=['POST', 'GET'])
# def get_user_activity_list():
#     activityManager = ActivityManager()
#     method = activityManager.getUserActivityList
#     return generate_call_back(method=method)
#
# #获取俱乐部活动列表
# @app.route('/get_club_activity_list/', methods=['POST', 'GET'])
# def get_club_activity_list():
#     activityManager = ActivityManager()
#     method = activityManager.getClubActivityList
#     return generate_call_back(method=method)
#
# #参加活动
# @app.route('/create_participate/', methods=['POST', 'GET'])
# def create_participate():
#     activityManager = ActivityManager()
#     method = activityManager.createParticipate
#     return generate_call_back(method=method)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5098)
