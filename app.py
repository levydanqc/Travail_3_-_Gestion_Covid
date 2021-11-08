from flask import Flask, request, session
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect
from werkzeug.wrappers import response
import config
from bd import db
from blueprint.cas.gestion_cas import routes_cas
from blueprint.comptes.gestion_comptes import routes_comptes
from blueprint.erreurs.gestion_erreurs import routes_erreurs
from babel.dates import format_date
from datetime import datetime


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config.DevelopmentConfig)
    app.register_blueprint(routes_cas)
    app.register_blueprint(routes_comptes)
    app.register_blueprint(routes_erreurs)

    compte = f'{app.config["DB_USERNAME"]}:{app.config["DB_PASSWORD"]}'
    serveur_bd = f'{app.config["DB_SERVEUR"]}/{app.config["DB_NAME"]}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"""mysql://{compte}@{serveur_bd}"""
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


def refresh_date():
    session['date'] = format_date(datetime.today(), format='medium', locale=(
        request.cookies.get('lang') or config['DEFAULT_LOCALE']))


@app.route('/')
def index():
    return redirect(url_for('gestion_cas.accueil'))


@app.route('/fr')
def fr():
    response = make_response(redirect(request.referrer or '/'))
    response.set_cookie('lang', 'fr_CA', max_age=60 * 60 * 24 * 365)
    return response


@app.route('/en')
def en():
    response = make_response(redirect(request.referrer or '/'))
    response.set_cookie('lang', 'en_CA', max_age=60 * 60 * 24 * 365)
    return response


@app.before_request
def before_request():
    refresh_date()


if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOST'])
