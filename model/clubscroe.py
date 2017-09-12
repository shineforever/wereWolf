from .flaskapp import db

class ClubScore(db.Model):
    __tablename__ = 'ClubScore'
    score_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100))
    club_number = db.Column(db.Integer)
    club_id = db.Column(db.String(100))

    def __init__(self, score_id=None, user_id=None, club_number=0, club_id=None):
        self.score_id = score_id
        self.user_id = user_id
        self.club_number = club_number
        self.club_id = club_id

    def __repr__(self):
        return self.score_id


    @staticmethod
    def create(info):
        score_id = info['score_id']
        user_id = info['user_id']
        club_number = info['club_number']
        club_id = info['club_id']
        club_score = ClubScore(
            score_id=score_id, user_id=user_id,
            club_id=club_id,club_number=club_number
        )
        db.session.add(club_score)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['score_id'] = result.score_id
        res['user_id'] = result.user_id
        res['club_number'] = result.club_number
        res['club_id'] = result.club_id
        return (True, res)
