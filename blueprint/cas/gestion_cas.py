""" Module de la gestion des cas. """
from babel.dates import format_date
from babel.numbers import format_number
from flask import Blueprint, abort, redirect, render_template, request, session
from flask.helpers import flash, url_for

from bd import db
from blueprint.cas.models.cas import Cas, Regions

routes_cas = Blueprint('gestion_cas', __name__,
                       url_prefix='/cas', template_folder='templates')


@routes_cas.route('/')
def accueil():
    """ Route de la page d'accueil.

    Returns:
        Render_template: La page d'accueil des cas
    """
    regions = Regions.query.order_by(Regions.nom).all()
    return render_template('liste_region.html', regions=regions, number=format_number)


@routes_cas.route('/admin')
def liste_admin():
    """ Route de la liste des cas détaillée.

    Returns:
        Render_template: La page de liste des cas
    """
    if not session.get('compte_id'):
        session['loginErreurs'] = {
            "username": "Vous devez être authentifié pour accéder à cette page"}
        session['url'] = url_for('gestion_cas.liste_admin')
        abort(401)
    cas = Cas.query.all()
    return render_template('liste_admin.html', lesCas=cas, regions=Regions, date=format_date)


@routes_cas.route('/creer', methods=['GET', 'POST'])
def creer_cas():
    """ Route de la création d'un cas.

    Returns:
        Render_template: La page de création d'un cas
    """
    if not session.get('compte_id'):
        session['loginErreurs'] = {
            "username": "Vous devez être authentifié pour accéder à cette page"}
        session['url'] = url_for('gestion_cas.creer_cas')
        abort(401)
    if request.method == 'POST':
        cas = Cas(
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            region=request.form.get('region'),
            compte=session.get('compte_id'),
        )
        if len(cas.erreurs) > 0:
            return render_template('saisie.html', cas=cas, messages=cas.erreurs,
                                   regions=Regions.query.order_by(Regions.nom).all())
        db.session.add(cas)
        db.session.commit()
        flash('Le cas a été créé avec succès', 'success')
        return render_template('saisie.html', sucess="Le cas a été créé avec succès.")
    return render_template('saisie.html', regions=Regions.query.order_by(Regions.nom).all())


@routes_cas.route('/<int:id>/delete', methods=['GET', 'POST'])
def supprimer_cas(id_cas):
    """ Route de la suppression d'un cas.

    Args:
        id (int): Id du cas à supprimer

    Returns:
        Http: Requête HTTP (Redirection)
    """
    if not session.get('admin'):
        session['url'] = url_for('gestion_cas.supprimer_cas')
        if not session.get('compte_id'):
            session['loginErreurs'] = {
                "username": "Vous devez être authentifié pour accéder à cette page"}
        abort(403)
    if request.method == 'POST':
        Cas.query.filter_by(id=id_cas).delete()
        db.session.commit()
        flash('Le cas a été supprimé avec succès.', 'success')
        return redirect(request.referrer or '/')
    return redirect(request.referrer or '/')
