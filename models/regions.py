from bd import db

class Regions(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    numero_region = db.Column(db.String(2), unique=True, nullable=False)
    nom = db.Column(db.String(45), unique=True, nullable=False)
    cas = db.relationship('Cas', backref='region', lazy=True)

    def __repr__(self):
        return 'Région: %s' % (self.nom)
