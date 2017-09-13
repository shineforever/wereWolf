# coding=utf8

VALIDITY = 7

WHOOSH_BASE = '/home/yz/work/werewolfSearchData/'

APP_ID = 'wx764d3845feee904a' #微信小程序APP, ID
APP_SECRET = '9eaf302b599dcae0d282854e5af88651' #微信小程序APP, secret

# APP_ID = 'wxddf05171165e98c6' #微信小程序APP, ID
# APP_SECRET = 'c2bac13f26d2a1adfd60de223b670080' #微信小程序APP, secret


GET_OPENID_URL = 'https://api.weixin.qq.com/sns/jscode2session'

WECHAT_USER_TAG = 1 #微信小程序用户tag

#==========================法官操作类型============================
OPERATE_ASSIGN_ROLE = '1'#分配玩家角色
OPERATE_START_ACTIVITY = '2'#开始活动
OPERATE_PARTICIPANT_OUT = '3'#玩家出局


#==========================活动中玩家角色============================
ROLE_JUDGE = '1'#法官
ROLE_VILLAGER = '2'#村民
ROLE_GOD_PEOPLE = '3'#神民
ROLE_WEREWOLF = '4'#狼人
ROLE_EMPTY = '0' #未分配
SCORE_WEREWOLF = {
    '1': 0,
    '2': 20,
    '3': 30,
    '4': -30
}
SCORE_VILLAGER = {
    '1': 0,
    '2': -20,
    '3': -30,
    '4': 30
}
SCORE_EMPTY = 0


#==========================活动状态============================
ACTIVITY_USER = 1 #普通活动
ACTIVITY_CLUB = 2 #俱乐部活动
ACTIVITY_CREATE_STATE = 1 #创建活动状态
ACTIVITY_ENTER_FULL_STATE = 2 #无法报名,名额已满状态
ACTIVITY_STATE_START = 3 #活动开始
ACTIVITY_STATE_SCORE = 4 #活动计分
ACTIVITY_STATE_END = 5 #活动结束


#==========================位置信息============================
EMPTY_LOCATION = 0


OSS_ACCESS_KEY_ID = 'LTAIHuzyjCL6eXhq'
OSS_ACCESS_KEY_SERCRET = 'mhMabaZEUJPAQbCW21Fm8HgprCy3gf'
OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'

#
# OSS_ACCESS_KEY_ID = 'HReEC1sQufBRLcQC'
# OSS_ACCESS_KEY_SERCRET = '5rqWY7jXhGeF0HBhYpl10mSkgrrHZt'
# OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'




