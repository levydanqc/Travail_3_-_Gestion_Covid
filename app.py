""" Module de création d'une application Web avec Flask et SQLAlchemy. """

from datetime import datetime

from babel.dates import format_date
from flask import Flask, request, session
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect

import config
from bd import db
from blueprint.cas.gestion_cas import routes_cas
from blueprint.comptes.gestion_comptes import routes_comptes
from blueprint.erreurs.gestion_erreurs import routes_erreurs


def create_app():
    """ Création de l'application Flask.

        Returns:
            Flask: l'application Flask
    """
    flask = Flask(__name__, template_folder='templates')
    flask.config.from_object(config.DevelopmentConfig)
    flask.register_blueprint(routes_cas)
    flask.register_blueprint(routes_comptes)
    flask.register_blueprint(routes_erreurs)

    compte = f'{flask.config["DB_USERNAME"]}:{flask.config["DB_PASSWORD"]}'
    serveur_bd = f'{flask.config["DB_SERVEUR"]}/{flask.config["DB_NAME"]}'
    flask.config['SQLALCHEMY_DATABASE_URI'] = f"""mysql://{compte}@{serveur_bd}"""
    flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(flask)
    return flask


app = create_app()


def refresh_date():
    """ Mise à jour de la date du jour. """
    lang = request.cookies.get('lang') or app.config['DEFAULT_LOCALE']
    session['date'] = format_date(
        datetime.today(), format='medium', locale=lang)


@app.route('/')
def index():
    """ Route de la page d'accueil.

    Returns:
        Reponse: Reponse HTTP (Redirection)
    """
    return redirect(url_for('gestion_cas.accueil'))


@app.route('/fr')
def fr_ca():
    """ Route du changement de la langue en Français.

    Returns:
        Response: Réponse HTTP (Redirection)
    """
    response = make_response(
        redirect(request.referrer or url_for('gestion_cas.accueil')))
    response.set_cookie('lang', 'fr_CA', max_age=60 * 60 * 24 * 365)
    return response


@app.route('/en')
def en_ca():
    """ Route du changement de la langue en Anglais.

    Returns:
        Response: Réponse HTTP (Redirection)
    """
    response = make_response(
        redirect(request.referrer or url_for('gestion_cas.accueil')))
    response.set_cookie('lang', 'en_CA', max_age=60 * 60 * 24 * 365)
    return response


@app.before_request
def before_request():
    """ Fonction d'appel avant chaque requête. """
    refresh_date()


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host=app.config['HOST'])
