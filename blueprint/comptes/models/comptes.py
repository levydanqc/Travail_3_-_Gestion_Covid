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

    @staticmethod
    def hash_pwd(password):
        return hashlib.sha256(password.encode()).hexdigest()[:45]

    def __init__(self, username, password, confirm):
        self.erreurs = {}
        self.compte = username
        self.password = self.hash_pwd(password)
        self.admin = False
        self.valider(confirm)

    def valider(self, confirm):
        if Comptes.query.filter_by(compte=self.compte).first():
            self.erreurs['compte'] = "Ce compte existe déjà"
        if len(self.compte) < 5:
            self.erreurs['username'] = "Le nom d'utilisateur doit contenir au moins 5 caractères"
        if len(self.password) < 5:
            self.erreurs['password'] = "Le mot de passe doit contenir au moins 5 caractères"
        if self.password != confirm:
            self.erreurs['confirm'] = "Les mots de passe ne correspondent pas."

    def __repr__(self):
        return 'Compte: %s' % (self.compte)
