# coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')

import json

from tool.Util import Util

from model.flask_app import db
from model.ImgPath import ImgPath

class ImageManager(Util):

    def __init__(self):
        pass

    # 获取图片列表
    def getImage(self, info):
        foreignID = info['foreignID']
        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        if info.has_key('directory'):
            directory = info['directory']
        else:
            directory = 'merchandise'
        query = db.session.query(ImgPath).filter(
            ImgPath.foreignID == foreignID
        )
        result = query.first()
        res = {}
        res['imgPathID'] = result.imgPathID
        ossInfo['objectKey'] = '%s/%s@!constrain-300h' % (directory, result.path)
        res['path'] = self.getSecurityUrl(ossInfo)
        return (True, res)
