from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from bd import db
from blueprint.cas.models.cas import Cas
from blueprint.cas.models.cas import Regions
from babel.dates import format_date
from babel.numbers import format_number

routes_cas = Blueprint('gestion_cas', __name__,
                       url_prefix='/cas', template_folder='templates')


@routes_cas.route('/')
def accueil():
    regions = Regions.query.all()
    return render_template('liste_region.html', regions=regions, number=format_number)


@ routes_cas.route('/cas')
def liste_admin():
    if not session.get('admin'):
        abort(403)
    cas = Cas.query.all()
    return render_template('liste_admin.html', lesCas=cas, regions=Regions, date=format_date)


@ routes_cas.route('/creer', methods=['GET', 'POST'])
def creer_cas():
    if not session.get('compte_id'):
        abort(401)
    if request.method == 'POST':
        cas = Cas(
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            region=request.form.get('region'),
            compte=session.get('compte_id'),
        )
        if len(cas.erreurs) > 0:
            return render_template('saisie.html', cas=cas, messages=cas.erreurs, regions=Regions.query.order_by(Regions.nom).all())
        db.session.add(cas)
        db.session.commit()
        return redirect(url_for('gestion_cas.creer_cas'), code=302)
    return render_template('saisie.html', regions=Regions.query.order_by(Regions.nom).all())


@ routes_cas.route('/<int:id>/delete', methods=['GET', 'POST'])
def supprimer_cas(id):
    if not session.get('compte_id'):
        abort(401)
    if not session.get('admin'):
        abort(403)
    if request.method == 'POST':
        id = 5
        Cas.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(request.referrer or '/')
    return redirect(request.referrer or '/')
