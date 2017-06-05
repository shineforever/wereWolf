# coding=utf8
import sys
import types
import xmltodict

reload(sys)
sys.setdefaultencoding('utf-8')
import json
import urllib2
import poster as poster
from tool.Util import Util

from test_by_yz_config import ResultManager
LOCALHOST = '127.0.0.1:5098'
REMOTE = '121.41.56.218'


# 后台，　创建后台管理员
def create_admin_info_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/create_admin_info_background/' % LOCALHOST
    util = Util()
    info = {}
    info['tel'] = '15951606335'
    info['adminName'] = '一曲广陵散'
    info['adminPW'] = util.getMD5String('123456')
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


# 后台，　管理员登录
def admin_login_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/admin_login_background/' % LOCALHOST
    util = Util()
    info = {}
    info['tel'] = '15951606335'
    info['adminPW'] = util.getMD5String('123456')
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

#后台，　创建用户
def create_user_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/create_user_background/' % LOCALHOST
    imgFile = open('/home/yz/Desktop/carousel/%s' % '3.jpg', 'rb')
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['userName'] = 'yz3'
    info['gender'] = 1
    info['longitude'] = 118.46
    info['latitude'] = 32.03
    info['userType'] = 1
    info['openID'] = ''
    params = {'data': json.dumps(info), 'imgFile': imgFile}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def get_user_info_detail_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/get_user_info_detail_background/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['userID'] = '2017-06-05084045d15890271661f08a0094d912b723f6dd'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_user_info_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/get_user_info_detail/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-05102533fca3a297139dd634a2a1cbe1358b433d'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def create_club_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/create_club_background/' % LOCALHOST
    imgFile = open('/home/yz/Desktop/carousel/%s' % '4.jpg', 'rb')
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['clubName'] = '测试俱乐部2'
    info['creatorName'] = '创建者2'
    info['provinceID'] = '10'
    info['cityID'] = '63'
    info['countyID'] = '1596'
    info['area'] = '苏果超市'
    info['longitude'] = 118.46
    info['latitude'] = 32.03
    params = {'data': json.dumps(info), 'imgFile': imgFile}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_club_detail_background():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/get_club_detail_background/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['clubID'] = '2017-06-0511085842296e285f769fb77327aa76df97c585'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_club_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/get_club_detail/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['clubID'] = '2017-06-0511085842296e285f769fb77327aa76df97c585'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result


def create_activity():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/create_activity/' % LOCALHOST
    imgFile = open('/home/yz/Desktop/carousel/%s' % '5.jpg', 'rb')
    info = {}
    info['tokenID'] = '2017-06-05102533fca3a297139dd634a2a1cbe1358b433d'
    info['activityName'] = '测试活动3'
    info['fee'] = '10元/人'
    info['entryStartDate'] = '2017-06-06'
    info['startDate'] = '2017-06-08'
    info['endDate'] = '2017-06-20'
    info['minNumber'] = 12
    info['area'] = '康华新村'
    info['description'] = '活动要求33'
    # info['typeID'] = 2
    # info['clubID'] = '2017-06-0514303538150aa1f65767d7424f61b84a18c3f3'
    params = {'data': json.dumps(info), 'imgFile': imgFile}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_activity_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/get_activity_detail/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['activityID'] = '2017-06-051358481b5d8588ea9e65f328854086551656b9'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_user_activity_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/get_user_activity_list/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def get_club_activity_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/get_club_activity_list/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
    info['startIndex'] = 0
    info['pageCount'] = 10
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

def create_participate():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s/create_participate/' % LOCALHOST
    info = {}
    info['tokenID'] = '2017-06-05102533fca3a297139dd634a2a1cbe1358b433c'
    info['activityID'] = '2017-06-051358481b5d8588ea9e65f328854086551656b9'
    params = {'data': json.dumps(info)}
    resultManager = ResultManager()
    result = resultManager.getResult(params, upload_url)
    print result

if __name__ == '__main__':
    # create_participate()
    get_club_activity_list()
    # get_user_activity_list()
    # get_activity_detail()
    # create_activity()
    # get_club_detail()
    # get_club_detail_background()
    # admin_login_background()
    # create_admin_info_background()
    # create_club_background()
    # create_user_background()
    # get_user_info_detail_background()
    # get_user_info_detail()