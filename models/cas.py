from bd import db
from models.regions import Regions


class Cas(db.Model):
    __tablename__ = "cas"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    prenom = db.Column(db.String(45), nullable=False)
    nom = db.Column(db.String(45), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)
    compte_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Nom: %s' % (self.nom[0]+self.prenom[0])

    def __init__(self, date, prenom, nom, region_id, compte_id):
        self.date = date
        self.prenom = prenom
        self.nom = nom
        self.region_id = region_id
        self.compte_id = compte_id

    def valider(self):
        """
        Valide la création d'un cas.
        """
        erreurs = []
        if self.nom is None or self.nom == "":
            erreurs["nom"] = "Le nom est obligatoire"
        elif len(self.nom) > 45:
            erreurs["nom"] = "Le nom ne doit pas avoir plus de 45 caractères"
        if self.region is None or self.region == "":
            erreurs["region"] = "La région est requise"
        else:
            region = Region.query.get(self.region)
            if region is None:
                erreurs["region"] = "La région est requise et doit être l'une des régions de la liste"

        return erreurs
