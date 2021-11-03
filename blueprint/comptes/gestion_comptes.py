from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from blueprint.comptes.comptes import Comptes
from bd import db

routes_comptes = Blueprint('gestion_comptes', __name__,
                           url_prefix='/comptes', template_folder='templates')


@routes_comptes.route('/signup')
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            db.session.add(Comptes(username=username, password=password))
            db.session.commit()
            return redirect(url_for('gestion_comptes.login'))
        return render_template('signup.html')
    return render_template('signup.html')
