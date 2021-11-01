from flask import Blueprint, render_template, request, redirect, url_for, flash

from models.cas import Cas
from models.regions import Regions
from bd import db

routes = Blueprint('gestion_cas', __name__,
                   url_prefix='/gestion_cas', template_folder='templates')


@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/liste/regions')
def afficher_cas(id):
    cas = Cas.query.get(id)
    return render_template('liste_region.html', cas=cas)


@routes.route('/liste/admin')
def afficher_cas(id):
    cas = Cas.query.get(id)
    return render_template('liste_admin.html', cas=cas)


@routes.route('/creer', methods=['GET', 'POST'])
def creer_cas():
    if request.method == 'POST':
        cas = Cas(
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            region=request.form.get('region'),
            compte=request.form.get('compte'),
            date=request.form.get('date'),
        )
        erreurs = cas.valider()
        if len(erreurs) > 0:
            # flash(erreurs, 'danger')
            return render_template('saisie.html', cas=cas, messages=erreurs, regions=Regions.query.order_by(Regions.nom).all())
        db.session.add(cas)
        db.session.commit()
        # flash('Cas créé avec succès !')
        return redirect(url_for('afficher_cas', id=request.form.get('id')))
    return render_template('saisie.html', regions=Regions.query.order_by(Regions.nom).all())


@routes.route('/<int:id>/modifier')
def modifier_cas(id):
    cas = Cas.query.get(id)
    if cas is None:
        return redirect(url_for('accueil'), code=404)
    if request.method == 'POST':
        cas.titre = request.form['titre']
        cas.description = request.form['description']
        cas.date_creation = request.form['date_creation']
        cas.date_cloture = request.form['date_cloture']
        cas.etat = request.form['etat']
        cas.id_utilisateur = request.form['id_utilisateur']
        db.session.commit()
        # flash('Cas modifié avec succès !')
        return redirect(url_for('gestion_cas.afficher_cas', id=cas.id))
    return render_template('modifier_cas.html', cas=cas)
