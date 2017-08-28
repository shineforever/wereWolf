from .flaskapp import db

class UserInfo(db.Model):
    __tablename__ = 'UserInfo'
    user_id = db.Column(db.String(100), primary_key=True)
    user_name = db.Column(db.String(100))
    open_id = db.Column(db.String(100))
    score = db.Column(db.Integer)
    createtime = db.Column(db.DateTime)

    participate = db.relationship('Participate', backref='UserInfo', lazy='dynamic')

    def __init__(self, user_id=None, open_id=None, user_name=None,
                 createtime=None, score=0):
        self.user_id = user_id
        self.open_id = open_id
        self.user_name = user_name
        self.score = score
        self.createtime = createtime

    def __repr__(self):
        return self.user_id


    @staticmethod
    def create(info):
        user_id = info['user_id']
        user_name = info['user_name']
        open_id = info['open_id']
        score = info['score']
        createtime = info['createtime']
        userinfo = UserInfo(
            user_id=user_id, user_name=user_name, score=score,
            open_id=open_id, createtime=createtime,
        )
        db.session.add(userinfo)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['user_id'] = result.user_id
        res['user_name'] = result.user_name
        res['open_id'] = result.open_id
        res['score'] = result.score
        res['createtime'] = str(result.createtime)
        return (True, res)

    @staticmethod
    def generate_brief(result):
        res = {}
        res['user_id'] = result.user_id
        res['user_name'] = result.user_name
        return (True, res)
