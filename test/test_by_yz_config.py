#coding:utf-8
import json
import oss2
import urllib2
import poster as poster

LOCALHOST = '127.0.0.1'
REMOTE = '121.43.111.75'
PORT = '5005'

class ResultManager():
    def __init__(self):
        pass
    def getResult(self, params, upload_url):
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(upload_url, datagen, headers)
        data = urllib2.urlopen(request)
        result = data.read()
        return result