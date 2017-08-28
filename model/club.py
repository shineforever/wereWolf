from .flaskapp import db

class Club(db.Model):
    __tablename__ = 'Club'
    club_id = db.Column(db.String(100), primary_key=True)
    club_name = db.Column(db.String(100))
    user_id = db.Column(db.String(100), db.ForeignKey('AdminInfo.admin_id'))
    area = db.Column(db.Text)
    createtime = db.Column(db.DateTime)

    def __init__(self, club_id=None, club_name=None,
                 user_id=None, area=None, createtime=None):
        self.club_id = club_id
        self.club_name = club_name
        self.user_id = user_id
        self.area = area
        self.createtime = createtime

    def __repr__(self):
        return self.club_id

    @staticmethod
    def create(info):
        club_id = info['club_id']
        club_name = info['club_name']
        user_id = info['user_id']
        area = info['area']
        createtime = info['createtime']
        club = Club(
            club_id=club_id, club_name=club_name,
            user_id=user_id, area=area, createtime=createtime
        )
        db.session.add(club)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['club_id'] = result.club_id
        res['club_name'] = result.club_name
        res['user_id'] = result.user_id
        res['area'] = result.area
        res['createtime'] = str(result.createtime)
        return (True, res)


