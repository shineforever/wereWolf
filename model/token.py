from .flaskapp import db

class Token(db.Model):
    __tablename__ = 'Token'
    token_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100))
    createtime = db.Column(db.DateTime)
    validity = db.Column(db.Integer)

    def __init__(self, token_id=None, user_id=None, createtime=None, validity=None):
        self.token_id = token_id
        self.user_id = user_id
        self.createtime = createtime
        self.validity = validity
        
    def __repr__(self):
        return self.token_id

    @staticmethod
    def create(info):
        token_id = info['token_id']
        user_id = info['user_id']
        createtime = info['createtime']
        validity = info['validity']
        token = Token(token_id=token_id, user_id=user_id, createtime=createtime, validity=validity)
        db.session.add(token)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['token_id'] = result.token_id
        res['user_id'] = result.user_id
        res['createtime'] = str(result.createtime)
        res['validity'] = result.validity
        return (True, res)

