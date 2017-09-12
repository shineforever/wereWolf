import inspect
import json
import requests
from datetime import datetime
import time


from tool.util import Util
from tool.error_config import ErrorInfo
LOCALHOST = '192.168.40.156:5098'
ADMIN_TOKNE_ID = '2017-08-290843211652ec5f85f20c297769be144a46ec49'

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
            error_info = ErrorInfo['WOLFS_20']
            error_info['detail'] = str(e)
            return (False, error_info)

def get_result_info(url, params):
    url = 'http://{0}/{1}/'.format(LOCALHOST, url)
    call_back_info = requests.post(url=url, data=params)
    call_back_data = json.loads(call_back_info.text)
    print('22222')
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
    with open('/home/yz/Desktop/carousel/%s' % 'club3.jpg', 'rb') as img_file:
        upload_info = {}
        upload_info['img_file'] = img_file
        upload_info['directory'] = 'club'
        (status, imgpath) = resultmanager.upload_image(upload_info=upload_info)
        if status is False:
            return (False, imgpath)
    info = {}
    info['token_id'] = ADMIN_TOKNE_ID
    info['imgpath'] = imgpath
    info['club_name'] = '天狼俱乐部'
    info['area'] = '雨山地铁站1号出口'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def create_user_background():
    resultmanager = ResultManager()
    with open('/home/yz/Desktop/carousel/user/%s' % '14.png', 'rb') as img_file:
        upload_info = {}
        upload_info['img_file'] = img_file
        upload_info['directory'] = 'user'
        (status, imgpath) = resultmanager.upload_image(upload_info=upload_info)
        if status is False:
            return (False, imgpath)
    info = {}
    info['token_id'] = ADMIN_TOKNE_ID
    info['imgpath'] = imgpath
    info['user_name'] = '欧洲短毛猫'
    info['open_id'] = '-1'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def create_activity_background():
    resultmanager = ResultManager()
    with open('/home/yz/Desktop/carousel/activity/%s' % '3.jpg', 'rb') as img_file:
        upload_info = {}
        upload_info['img_file'] = img_file
        upload_info['directory'] = 'activity'
        (status, imgpath) = resultmanager.upload_image(upload_info=upload_info)
        if status is False:
            return (False, imgpath)
    info = {}
    info['token_id'] = ADMIN_TOKNE_ID
    info['activity_name'] = '狼人杀活动3'
    info['startdate'] = '2017-9-18'
    info['description'] = '狼人杀活动3描述'
    info['min_number'] = 5
    info['max_number'] = 10
    info['fee'] = '免费'
    info['imgpath'] = imgpath
    info['area'] = '南京先锋书店'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def create_participate():
    info = {}
    info['token_id'] = '2017-08-2910184210f721ec57542ec6bf6ebf719b72d125'
    info['activity_id'] = '2017-09-11153106fb803f758d4088b49fd659a9cf2ff5b6'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def create_roletype_background():
    info = {}
    info['token_id'] = ADMIN_TOKNE_ID
    info['type_id'] = '4'
    info['type_name'] = '神民'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def create_judge():
    info = {}
    info['token_id'] = '2017-08-291022328bed8c60e1e8795519211fd1aea20aec'
    info['activity_id'] = '2017-08-29100733f148d6edc0e4438e69d27019ec0403be'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def assign_role():
    info = {}
    info['token_id'] = '2017-08-291022328bed8c60e1e8795519211fd1aea20aec'
    info['foreign_id_list'] = ['2017-08-291019586fb5300a08540597c3061456d6f10e36']
    info['roletype_id'] = '4'
    info['activity_id'] = '2017-08-29100733f148d6edc0e4438e69d27019ec0403be'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def revoke_operate():
    info = {}
    info['token_id'] = '2017-08-291022328bed8c60e1e8795519211fd1aea20aec'
    info['activity_id'] = '2017-08-29100733f148d6edc0e4438e69d27019ec0403be'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def start_activity():
    info = {}
    info['token_id'] = '2017-08-291022328bed8c60e1e8795519211fd1aea20aec'
    info['activity_id'] = '2017-08-29100733f148d6edc0e4438e69d27019ec0403be'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def participant_out():
    info = {}
    info['token_id'] = '2017-08-291022328bed8c60e1e8795519211fd1aea20aec'
    info['activity_id'] = '2017-08-29100733f148d6edc0e4438e69d27019ec0403be'
    info['foreign_id'] = '2017-08-29102121d5fa5342d2fe47d86b5aeb72b44e0797'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def wechat_login():
    info = {}
    info['token_id'] = '2017-08-291022328bed8c60e1e8795519211fd1aea20aec'
    info['activity_id'] = '2017-08-29100733f148d6edc0e4438e69d27019ec0403be'
    info['foreign_id'] = '2017-08-29102121d5fa5342d2fe47d86b5aeb72b44e0797'
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)

def get_activity_list():
    print('11111')
    info = {}
    info['token_id'] = '2017-08-291022328bed8c60e1e8795519211fd1aea20aec'
    info['type_id'] = 1
    info['start_index'] = 0
    info['page_count'] = 10
    params = {'data': json.dumps(info)}
    get_result_info(url=inspect.stack()[0][3], params=params)


if __name__ == '__main__':
    # t1 = datetime.now()
    # print(t1)
    # time.sleep(0.01)
    # t2 = datetime.now()
    # print(t2-t1)
    # t3 = datetime.now()
    # print(t3)
    # for i in range(100):
    #     time.sleep(0.01)
    # t4 = datetime.now()
    # print(t4-t3)
    # t1 = datetime.now()
    # print(t1)
    # get_activity_list()
    # t2 = datetime.now()
    # print(t2-t1)
    # t3 = datetime.now()
    # print(t3)
    # for i in range(100):
    #     get_activity_list()
    # t4 = datetime.now()
    # print(t4-t3)
    # wechat_login()
    # participant_out()
    # start_activity()
    # revoke_operate()
    # assign_role()
    # create_judge()
    # create_roletype_background()
    create_participate()
    # create_admin_info_background()
    # admin_login_background()
    # create_club_background()
    # create_user_background()
    # create_activity_background()






