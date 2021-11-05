from flask import Blueprint, render_template, request, redirect, url_for, session
from blueprint.comptes.models.comptes import Comptes
from bd import db

routes_comptes = Blueprint('gestion_comptes', __name__,
                           url_prefix='/comptes', template_folder='templates')


@routes_comptes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        compte = Comptes(username=request.form.get('username'),
                         password=request.form.get('password'), confirm=request.form.get('confirm'))
        if len(compte.erreurs) > 0:
            session['signupErreurs'] = compte.erreurs
            return redirect(request.referrer if request.referrer else '/')
        db.session.add(compte)
        db.session.commit()
        session['connected'] = True
        if request.form.get('rememberMe') == 'on':
            session.permanent = True
        else:
            session.permanent = False
        return redirect(request.referrer if request.referrer else '/')
    return redirect(request.referrer if request.referrer else '/')


@routes_comptes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        erreurs = {}
        compte = Comptes.query.filter_by(compte=request.form.get(
            'username'), password=request.form.get('password')).first()
        if compte is None:
            erreurs["username"] = "Le nom d'utilisateur ou le mot de passe n'est pas valide"
        if len(erreurs) > 0:
            session['loginErreurs'] = erreurs
            return redirect(request.referrer if request.referrer else '/')
        session['connected'] = True
        if request.form.get('rememberMe') == 'on':
            session.permanent = True
        else:
            session.permanent = False
    return redirect(request.referrer if request.referrer else '/')


@routes_comptes.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(request.referrer if request.referrer else '/')