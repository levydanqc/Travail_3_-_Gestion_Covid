from bd import db
import re
import hashlib


class Comptes(db.Model):
    __tablename__ = "comptes"

    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, nullable=False)
    compte = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), unique=True, nullable=False)
    cas = db.relationship('Cas', backref='comptes', lazy=True)

    erreurs = {}

    def __init__(self, username, password, confirm):
        self.erreurs = {}
        self.valider(confirm)
        self.compte = username
        self.password = self.hash_pwd(password)
        self.admin = False

    def hash_pwd(password):
        return hashlib.sha256(password.encode()).hexdigest()[:45]

    def valider(self, confirm):
        if Comptes.query.filter_by(compte=self.compte).first():
            self.erreurs['compte'] = "Ce compte existe déjà"
        if not re.compile("""(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""").match(self.compte):
            self.erreurs['username'] = "Votre adresse email n'est pas valide"
        if not re.compile('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#\?&^_-]).{8,}').match(self.password):
            self.erreurs['password'] = "Votre mot de passe doit contenir au moins 8 caractères, 1 majuscule, 1 minuscule, 1 chiffre et 1 caractère spécial"
        if self.password != confirm:
            self.erreurs['confirm'] = "Les mots de passe ne correspondent pas."

    def __repr__(self):
        return 'Compte: %s' % (self.compte)
