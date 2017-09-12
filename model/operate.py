from .flaskapp import db

class Operate(db.Model):
    __tablename__ = 'Operate'
    operate_id = db.Column(db.String(100), primary_key=True)
    foreign_id = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    activity_id = db.Column(db.String(100))
    type_id = db.Column(db.String(100))
    level_number = db.Column(db.Integer)
    createtime = db.Column(db.DateTime)

    def __init__(self, operate_id=None, foreign_id=None, activity_id=None,
                 createtime=None, type_id=None, user_id=None,
                 level_number=0):
        self.operate_id = operate_id
        self.foreign_id = foreign_id
        self.user_id = user_id
        self.activity_id = activity_id
        self.type_id = type_id
        self.level_number = level_number
        self.createtime = createtime

    def __repr__(self):
        return self.operate_id

    @staticmethod
    def create(info):
        operate_id = info['operate_id']
        foreign_id = info['foreign_id']
        user_id = info['user_id']
        activity_id = info['activity_id']
        createtime = info['createtime']
        level_number = info['level_number']
        type_id = info['type_id']
        operate = Operate(
            operate_id=operate_id, foreign_id=foreign_id, activity_id=activity_id,
            createtime=createtime, user_id=user_id, level_number=level_number,
            type_id=type_id
        )
        db.session.add(operate)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['operate_id'] = result.operate_id
        res['foreign_id'] = result.foreign_id
        res['user_id'] = result.user_id
        res['activity_id'] = result.activity_id
        res['createtime'] = str(result.createtime)
        res['level_number'] = result.level_number
        res['type_id'] = result.type_id
        return (True, res)
