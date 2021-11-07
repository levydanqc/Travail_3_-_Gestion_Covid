from flask import Flask, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
import config
from config import SessionMiddleware
from bd import db
from blueprint.cas.gestion_cas import routes_cas
from blueprint.comptes.gestion_comptes import routes_comptes
from blueprint.gestion_erreurs import routes_erreurs


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config.DevelopmentConfig)
    app.wsgi_app = SessionMiddleware(app.wsgi_app, prefix='/gestion_covid')
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


@app.route('/')
def index():
    return redirect(url_for('gestion_cas.accueil'))


@app.route('/fr')
def fr():
    session['lang'] = 'fr'
    return redirect(request.referrer or '/')


@app.route('/en')
def en():
    session['lang'] = 'en'
    return redirect(request.referrer or '/')


if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOST'])
