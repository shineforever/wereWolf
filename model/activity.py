from .flaskapp import db

class Activity(db.Model):
    __tablename__ = 'Activity'
    activity_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('UserInfo.user_id'))
    activity_name = db.Column(db.String(100))
    fee = db.Column(db.String(100))
    startdate = db.Column(db.DateTime)
    activity_number = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    club_id = db.Column(db.String(100), db.ForeignKey('Club.club_id'))
    description = db.Column(db.Text)
    area =db.Column(db.Text)
    createtime = db.Column(db.DateTime)
    activity_state = db.Column(db.Integer)

    participate = db.relationship('Participate', backref='Activity', lazy='dynamic')

    def __init__(self, activity_id=None, user_id=None, startdate=None,
                 activity_name=None, activity_number=1,
                 type_id=None, club_id=None, description=None,
                 area=None, createtime=None, fee=None, activity_state=True):
        self.activity_id = activity_id
        self.user_id = user_id
        self.startdate = startdate
        self.activity_name = activity_name
        self.activity_number = activity_number
        self.type_id = type_id
        self.club_id = club_id
        self.description = description
        self.area = area
        self.createtime = createtime
        self.fee = fee
        self.activity_state = activity_state

    def __repr__(self):
        return self.activity_id


    @staticmethod
    def create(info):
        activity_id = info['activity_id']
        activity_name = info['activity_name']
        user_id = info['user_id']
        startdate = info['startdate']
        activity_number = info['activity_number']
        type_id = info['type_id']
        club_id = info['club_id']
        description = info['description']
        area = info['area']
        createtime = info['createtime']
        fee = info['fee']
        activity = Activity(
            activity_id=activity_id, activity_name=activity_name, user_id=user_id,
            startdate=startdate, activity_number=activity_number,
            type_id=type_id, club_id=club_id, description=description,
            area=area, createtime=createtime, fee=fee
        )
        db.session.add(activity)
        return (True, None)


    @staticmethod
    def generate(result):
        res = {}
        res['activity_id'] = result.activity_id
        res['activity_name'] = result.activity_name
        res['description'] = result.description
        res['area'] = result.area
        res['fee'] = result.fee
        res['startdate'] = str(result.startdate)
        res['createtime'] = str(result.createtime)
        res['activity_state'] = result.activity_state
        res['activity_number'] = result.activity_number
        res['type_id'] = result.type_id
        return (True, res)




