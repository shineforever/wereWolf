from .flaskapp import db

class AdminInfo(db.Model):
    __tablename__ = 'AdminInfo'
    admin_id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    admin_name = db.Column(db.String(100))
    tel = db.Column(db.String(100))

    def __init__(self, admin_id=None, admin_name=None, password=None, tel=None):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.password = password
        self.tel = tel

    def __repr__(self):
        return self.admin_id

    @staticmethod
    def create(info):
        admin_id = info['admin_id']
        admin_name = info['admin_name']
        password = info['password']
        tel = info['tel']
        admininfo = AdminInfo(admin_id=admin_id, admin_name=admin_name,
                              password=password, tel=tel)
        db.session.add(admininfo)
        return (True, None)

    @staticmethod
    def generate(result):
        res = {}
        res['admin_id'] = result.admin_id
        res['admin_name'] = result.admin_name
        res['password'] = result.password
        res['tel'] = result.tel
        return (True, res)
