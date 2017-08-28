import inspect
import json
import requests


from tool.util import Util
from tool.error_config import ErrorInfo
LOCALHOST = '127.0.0.1:5098'
ADMIN_TOKNE_ID = '2017-08-28143623dd5796eba37684aaa916775b02ad1107'

class ResultManager(Util):

    def upload_image(self, upload_info):
        try:
            img_file = upload_info['img_file']
            oss_info = {}
            oss_info['bucket'] = 'were-wolf'
            img_name = img_file.name
            _l = img_name.split(".")
            if len(_l) > 0:
                postfix = _l[-1]
            else:
                postfix = 'png'
            imgpath = self.generate_id(img_name) + '.' + postfix
            print(imgpath)
            info = {}
            directory = upload_info['directory']
            info['img_name'] = '{0}/{1}'.format(directory, imgpath)
            info['oss_info'] = oss_info
            info['img_file'] = img_file
            self.upload_oss_image(info)
            return (True, imgpath)
        except Exception as e:
            errorInfo = ErrorInfo['WOLFS_20']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

def get_result_info(url, params):
    url = 'http://{0}/{1}/'.format(LOCALHOST, url)
    call_back_info = requests.post(url=url, data=params)
    call_back_data = json.loads(call_back_info.text)
    print(call_back_data)



def create_admin_info_background():
    util = Util()
    info = {}
    info['tel'] = '15951606335'
    info['admin_name'] = '一曲广陵散'
    info['password'] = util.get_md5_string('123456')
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def admin_login_background():
    util = Util()
    info = {}
    info['tel'] = '15951606335'
    info['password'] = util.get_md5_string('123456')
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def create_club_background():
    resultmanager = ResultManager()
    with open('/home/yz/Desktop/carousel/%s' % 'club2.jpg', 'rb') as img_file:
        upload_info = {}
        upload_info['img_file'] = img_file
        upload_info['directory'] = 'club'
        (status, imgpath) = resultmanager.upload_image(upload_info=upload_info)
        if status is False:
            return (False, imgpath)
    info = {}
    info['token_id'] = ADMIN_TOKNE_ID
    info['imgpath'] = imgpath
    info['club_name'] = '苏果超市'
    info['area'] = '苏果超市地址'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)


if __name__ == '__main__':
    # create_admin_info_background()
    # admin_login_background()
    create_club_background()





















# import types
# import xmltodict
#
# sys.setdefaultencoding('utf-8')
# import json
# # import urllib2
# # import poster as poster
# from tool.util import Util
#
# from .test_by_yz_config import ResultManager
# LOCALHOST = '127.0.0.1:5098'
# REMOTE = '121.41.56.218'





# # 后台，　创建后台管理员
# def create_admin_info_background():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/create_admin_info_background/' % LOCALHOST
#     util = Util()
#     info = {}
#     info['tel'] = '15951606335'
#     info['adminName'] = '一曲广陵散'
#     info['adminPW'] = util.getMD5String('123456')
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
#
# # 后台，　管理员登录
# def admin_login_background():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/admin_login_background/' % LOCALHOST
#     util = Util()
#     info = {}
#     info['tel'] = '15951606335'
#     info['adminPW'] = util.getMD5String('123456')
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# #后台，　创建用户
# def create_user_background():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/create_user_background/' % LOCALHOST
#     imgFile = open('/home/yz/Desktop/carousel/%s' % '3.jpg', 'rb')
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['userName'] = 'yz3'
#     info['gender'] = 1
#     info['longitude'] = 118.46
#     info['latitude'] = 32.03
#     info['userType'] = 1
#     info['openID'] = ''
#     params = {'data': json.dumps(info), 'imgFile': imgFile}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
#
# def get_user_info_detail_background():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/get_user_info_detail_background/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['userID'] = '2017-06-05084045d15890271661f08a0094d912b723f6dd'
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def get_user_info_detail():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/get_user_info_detail/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-05102533fca3a297139dd634a2a1cbe1358b433d'
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def create_club_background():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/create_club_background/' % LOCALHOST
#     imgFile = open('/home/yz/Desktop/carousel/%s' % '4.jpg', 'rb')
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['clubName'] = '测试俱乐部2'
#     info['creatorName'] = '创建者2'
#     info['provinceID'] = '10'
#     info['cityID'] = '63'
#     info['countyID'] = '1596'
#     info['area'] = '苏果超市'
#     info['longitude'] = 118.46
#     info['latitude'] = 32.03
#     params = {'data': json.dumps(info), 'imgFile': imgFile}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def get_club_detail_background():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/get_club_detail_background/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['clubID'] = '2017-06-0511085842296e285f769fb77327aa76df97c585'
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def get_club_detail():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/get_club_detail/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['clubID'] = '2017-06-0511085842296e285f769fb77327aa76df97c585'
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
#
# def create_activity():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/create_activity/' % LOCALHOST
#     imgFile = open('/home/yz/Desktop/carousel/%s' % '5.jpg', 'rb')
#     info = {}
#     info['tokenID'] = '2017-06-05102533fca3a297139dd634a2a1cbe1358b433d'
#     info['activityName'] = '测试活动3'
#     info['fee'] = '10元/人'
#     info['entryStartDate'] = '2017-06-06'
#     info['startDate'] = '2017-06-08'
#     info['endDate'] = '2017-06-20'
#     info['minNumber'] = 12
#     info['area'] = '康华新村'
#     info['description'] = '活动要求33'
#     # info['typeID'] = 2
#     # info['clubID'] = '2017-06-0514303538150aa1f65767d7424f61b84a18c3f3'
#     params = {'data': json.dumps(info), 'imgFile': imgFile}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def get_activity_detail():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/get_activity_detail/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['activityID'] = '2017-06-051358481b5d8588ea9e65f328854086551656b9'
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def get_user_activity_list():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/get_user_activity_list/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['startIndex'] = 0
#     info['pageCount'] = 10
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def get_club_activity_list():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/get_club_activity_list/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-01104104a92fba33252db775d4b869b3ab5cfab1'
#     info['startIndex'] = 0
#     info['pageCount'] = 10
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# def create_participate():
#     opener = poster.streaminghttp.register_openers()
#     upload_url = 'http://%s/create_participate/' % LOCALHOST
#     info = {}
#     info['tokenID'] = '2017-06-05102533fca3a297139dd634a2a1cbe1358b433c'
#     info['activityID'] = '2017-06-051358481b5d8588ea9e65f328854086551656b9'
#     params = {'data': json.dumps(info)}
#     resultManager = ResultManager()
#     result = resultManager.getResult(params, upload_url)
#     print result
#
# if __name__ == '__main__':
#     # create_participate()
#     get_club_activity_list()
#     # get_user_activity_list()
#     # get_activity_detail()
#     # create_activity()
#     # get_club_detail()
#     # get_club_detail_background()
#     # admin_login_background()
#     # create_admin_info_background()
#     # create_club_background()
#     # create_user_background()
#     # get_user_info_detail_background()
#     # get_user_info_detail()