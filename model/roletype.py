from .flaskapp import db

class RoleType(db.Model):
    __tablename__ = 'RoleType'
    type_id = db.Column(db.String(100), primary_key=True)
    type_name = db.Column(db.String(100))

    def __init__(self, type_id=None, type_name=None):
        self.type_id = type_id
        self.type_name = type_name

    def __repr__(self):
        return self.type_id

    @staticmethod
    def create(info):
        type_id = info['type_id']
        type_name = info['type_name']
        roletype = RoleType(type_id=type_id, type_name=type_name)
        db.session.add(roletype)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['type_id'] = result.type_id
        res['type_name'] = result.type_name
        return (True, res)

