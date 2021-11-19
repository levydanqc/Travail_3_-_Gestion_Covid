""" Module de gestion des comptes. """
from flask import Blueprint, request, redirect, url_for, session, \
    render_template, flash, abort

from blueprint.comptes.models.comptes import Comptes
from bd import db

routes_comptes = Blueprint('gestion_comptes', __name__,
                           url_prefix='/comptes', template_folder='templates')


@routes_comptes.route('/')
def index():
    """ Route de la page d'accueil des comptes.

    Returns:
        Render_template: La page d'accueil des comptes
    """
    if not session.get('admin'):
        session['url'] = url_for('gestion_comptes.index')
        if not session.get('compte_id'):
            session['loginErreurs'] = {
                "username": "Vous devez être authentifié pour accéder à cette page"}
        abort(403)
    return render_template('comptes.html', comptes=Comptes.query.all())


@routes_comptes.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    """ Route de la création d'un compte.

    Returns:
        HttpResponse: La page d'accueil (Redirection)
    """
    if not session.get('admin'):
        session['url'] = url_for('gestion_comptes.ajouter')
        if not session.get('compte_id'):
            session['loginErreurs'] = {
                "username": "Vous devez être authentifié pour accéder à cette page"}
        abort(403)
    compte = Comptes(username=request.form.get('username'),
                     password=request.form.get('password'), confirm=request.form.get('confirm'))
    db.session.add(compte)
    db.session.commit()
    flash("Le compte à était ajouté avec succès", "success")
    return redirect(url_for('gestion_comptes.index'))


@routes_comptes.route('/supprimer/<int:id>', methods=['GET', 'POST'])
def delete(id_compte):
    """ Route de la suppression d'un compte.

    Args:
        id (int): Id du compte à supprimer

    Returns:
        HttpResponse: La page d'accueil (Redirection)
    """
    if not session.get('admin'):
        session['url'] = url_for('gestion_comptes.ajouter')
        if not session.get('compte_id'):
            session['loginErreurs'] = {
                "username": "Vous devez être authentifié pour accéder à cette page"}
        abort(403)
    compte = Comptes.query.get(id_compte)
    db.session.delete(compte)
    db.session.commit()
    flash("Le compte à était supprimé avec succès", "success")
    return redirect(url_for('gestion_comptes.index'))


@routes_comptes.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Route de la création d'un compte.

    Returns:
        HttpResponse: La page précédante (Redirection) ou la page d'accueil (Redirection)
    """
    if request.method == 'POST':
        compte = Comptes(username=request.form.get('username'),
                         password=request.form.get('password'), confirm=request.form.get('confirm'))
        if len(compte.erreurs) > 0:
            session['signupErreurs'] = compte.erreurs
            return redirect(request.referrer or url_for('gestion_cas.accueil'))
        db.session.add(compte)
        db.session.commit()
        session['compte_id'] = compte.id
        session['admin'] = compte.admin
        if request.form.get('rememberMe') == 'on':
            session.permanent = True
        else:
            session.permanent = False
        return redirect(request.referrer or url_for('gestion_cas.accueil'))
    return redirect(request.referrer or url_for('gestion_cas.accueil'))


@routes_comptes.route('/login', methods=['GET', 'POST'])
def login():
    """ Route de la connexion d'un compte.

    Returns:
        HttpResponse: La page précédante (Redirection) ou la page d'accueil (Redirection)
    """
    if request.method == 'POST':
        erreurs = {}
        compte = Comptes.query.filter_by(compte=request.form.get(
            'username'), password=Comptes.hash_pwd(request.form.get('password'))).first()
        if compte is None:
            erreurs["username"] = "Le nom d'utilisateur ou le mot de passe n'est pas valide"
        if len(erreurs) > 0:
            session['loginErreurs'] = erreurs
            return redirect(request.referrer or url_for('gestion_cas.accueil'))
        session['compte_id'] = compte.id
        session['admin'] = compte.admin
        if request.form.get('rememberMe') == 'on':
            session.permanent = True
        else:
            session.permanent = False

        return redirect(session.get('url') or url_for('gestion_cas.liste_admin'))
    return redirect(request.referrer or url_for('gestion_cas.accueil'))


@routes_comptes.route('/logout', methods=['GET', 'POST'])
def logout():
    """ Route de la déconnexion d'un compte.

    Returns:
        HttpResponse: La page d'accueil (Redirection)
    """
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('gestion_cas.accueil'))
    return redirect(url_for('gestion_cas.accueil'))
