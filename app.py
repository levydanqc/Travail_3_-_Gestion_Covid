from flask import Flask
from flask.templating import render_template
import config
from bd import db
from blueprint.gestion_cas.gestion_cas import routes


def create_app():
    app_flask = Flask(__name__, template_folder="blueprint/gestion_cas")
    app_flask.config.from_object(config.DevelopmentConfig)
    app_flask.register_blueprint(routes)
    compte = f'{app_flask.config["DB_USERNAME"]}:{app_flask.config["DB_PASSWORD"]}'
    serveur_bd = f'{app_flask.config["DB_SERVEUR"]}/{app_flask.config["DB_NAME"]}'
    app_flask.config['SQLALCHEMY_DATABASE_URI'] = f"""mysql://{compte}@{serveur_bd}""" 
    app_flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app_flask)
    return app_flask


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
