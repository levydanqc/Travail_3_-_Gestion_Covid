from bd import db
from blueprint.cas.models.regions import Regions
import datetime as dt


class Cas(db.Model):
    __tablename__ = "cas"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    prenom = db.Column(db.String(45), nullable=False)
    nom = db.Column(db.String(45), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey(
        'regions.id'), nullable=False)
    compte_id = db.Column(db.Integer, db.ForeignKey(
        'comptes.id'), nullable=False)
    erreurs = {}

    def __repr__(self):
        return self.prenom[0]+self.nom[0]

    def __init__(self, prenom, nom, region, compte):
        self.erreurs = {}
        self.date = dt.datetime.now()
        self.prenom = prenom.capitalize()
        self.nom = nom.capitalize()
        self.region_id = region
        self.compte_id = compte
        self.valider()

    def valider(self):
        """
        Valide la création d'un cas.
        """
        if self.nom is None or self.nom == "":
            self.erreurs["nom"] = "Le nom est obligatoire"
        elif len(self.nom) > 45:
            self.erreurs["nom"] = "Le nom ne doit pas avoir plus de 45 caractères"
        if self.prenom is None or self.prenom == "":
            self.erreurs["prenom"] = "Le prenom est obligatoire"
        elif len(self.prenom) > 45:
            self.erreurs["prenom"] = "Le prenom ne doit pas avoir plus de 45 caractères"
        if self.region_id is None or self.region_id == "":
            self.erreurs["region"] = "La région est requise"
        else:
            region = Regions.query.get(self.region_id)
            if region is None:
                self.erreurs["region"] = "La région est requise et doit être l'une des régions de la liste"
