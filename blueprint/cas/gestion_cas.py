from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from bd import db
from blueprint.cas.models.cas import Cas
from blueprint.cas.models.cas import Regions

routes_cas = Blueprint('gestion_cas', __name__,
                       url_prefix='/cas', template_folder='templates')


@routes_cas.route('/')
def accueil():
    regions = Regions.query.all()
    cas = {}
    for region in regions:
        cas[region.nom] = Cas.query.filter_by(region_id=region.id).count()
    return render_template('liste_region.html', cas=cas)


@routes_cas.route('/cas')
def liste_admin():
    cas = Cas.query.all()
    return render_template('liste_admin.html', cas=cas)


@routes_cas.route('/creer', methods=['GET', 'POST'])
def creer_cas():
    if request.method == 'POST':
        cas = Cas(
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            region=request.form.get('region'),
            compte=0,
        )
        if len(cas.erreurs) > 0:
            # flash(erreurs, 'danger')
            return render_template('saisie.html', cas=cas, messages=cas.erreurs, regions=Regions.query.order_by(Regions.nom).all())
        db.session.add(cas)
        db.session.commit()
        # flash('Cas créé avec succès !')
        return redirect(url_for('creer_cas'))
    return render_template('saisie.html', regions=Regions.query.order_by(Regions.nom).all(), connected=session.get('connected'))


@routes_cas.route('/<int:id>/modifier')
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
