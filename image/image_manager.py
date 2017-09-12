import sys
sys.path.append('..')

import json

from tool.util import Util
from tool.error_config import ErrorInfo
from model.flaskapp import db
from model.imgpath import ImgPath

class ImageManager(Util):

    def __init__(self):
        super().__init__()

    def upload_image(self, upload_info):
        # try:
        img_file = upload_info['img_file']
        oss_info = {}
        oss_info['bucket'] = 'were-wolf'
        img_name = img_file.filename
        _l = img_name.split(".")
        if len(_l) > 0:
            postfix = _l[-1]
        else:
            postfix = 'png'
        imgpath = self.generate_id(img_name) + '.' + postfix
        info = {}
        directory = upload_info['directory']
        info['img_name'] = '{0}/{1}'.format(directory, imgpath)
        info['oss_info'] = oss_info
        info['img_file'] = img_file
        self.upload_oss_image(info)
        return (True, imgpath)
        # except Exception as e:
        #     error_info = ErrorInfo['WOLFS_20']
        #     error_info['detail'] = str(e)
        #     return (False, error_info)

    def get_image(self, info):
        '''
        获取图片
        :param info: {'token_id': '', 'user_name': '', 'imgpath': '', 'user_id': '', 'open_id': ''}
        :return: {'data': '', 'status': 'SUCCESS'}
        '''
        res = {}
        foreign_id = info['foreign_id']
        oss_info = {}
        oss_info['bucket'] = 'were-wolf'
        if 'directory' in info:
            directory = info['directory']
        else:
            directory = 'user'
        query = db.session.query(ImgPath).filter(
            ImgPath.foreign_id == foreign_id
        )
        result = query.first()
        if result is None:
            res['imgpath'] = None
        else:
            res['imgpath_id'] = result.imgpath_id
            oss_info['object_key'] = '%s/%s' % (directory, result.imgpath)
            res['imgpath'] = self.get_security_url(oss_info)
        return (True, res)
