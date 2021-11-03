from bd import db


class Comptes(db.Model):
    __tablename__ = "comptes"

    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, nullable=False)
    compte = db.Column(db.String(45), unique=True, nullable=False)
    cas = db.relationship('Cas', backref='comptes', lazy=True)

    def __init__(self, username, password):
        self.compte = username + ':' + password
        self.admin = False
        
    def __repr__(self):
        return 'Compte: %s' % (self.compte)
