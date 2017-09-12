from .flaskapp import db

class Participate(db.Model):
    __tablename__ = 'Participate'
    participate_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('UserInfo.user_id'))
    activity_id = db.Column(db.String(100), db.ForeignKey('Activity.activity_id'))
    location = db.Column(db.Integer)
    roletype_id = db.Column(db.String(100))
    score = db.Column(db.Integer)
    state = db.Column(db.Boolean)
    createtime = db.Column(db.DateTime)

    def __init__(self, participate_id=None, user_id=None, activity_id=None,
                 createtime=None, location=None, roletype_id=None, state=False,
                 score=0):
        self.participate_id = participate_id
        self.user_id = user_id
        self.location = location
        self.activity_id = activity_id
        self.roletype_id = roletype_id
        self.score = score
        self.state = state
        self.createtime = createtime

    def __repr__(self):
        return self.participate_id

    @staticmethod
    def create(info):
        participate_id = info['participate_id']
        user_id = info['user_id']
        activity_id = info['activity_id']
        createtime = info['createtime']
        roletype_id = info['roletype_id']
        location = info['location']
        participate = Participate(
            participate_id=participate_id, user_id=user_id, activity_id=activity_id,
            createtime=createtime, location=location, roletype_id=roletype_id
        )
        db.session.add(participate)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['participate_id'] = result.participate_id
        res['user_id'] = result.user_id
        res['activity_id'] = result.activity_id
        res['location'] = result.location
        res['createtime'] = str(result.createtime)
        res['score'] = result.score
        res['roletype_id'] = result.roletype_id
        res['state'] = result.state
        return (True, res)
