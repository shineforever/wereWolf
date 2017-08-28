from .flaskapp import db

class ImgPath(db.Model):
    __tablename__ = 'ImgPath'
    imgpath_id = db.Column(db.String(100), primary_key=True)
    imgpath = db.Column(db.String(1000))
    foreign_id = db.Column(db.String(100))

    def __init__(self, imgpath_id=None, imgpath=None, foreign_id=None):
        self.imgpath_id = imgpath_id
        self.imgpath = imgpath
        self.foreign_id = foreign_id

    def __repr__(self):
        return self.imgpath_id

    @staticmethod
    def create(info):
        imgpath_id = info['imgpath_id']
        imgpath = info['imgpath']
        foreign_id = info['foreign_id']
        imgpath = ImgPath(imgpath_id=imgpath_id, imgpath=imgpath, foreign_id=foreign_id)
        db.session.add(imgpath)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['imgpath_id'] = result.imgpath_id
        res['imgpath'] = result.imgpath
        res['foreign_id'] = result.foreign_id
        return (True, res)




