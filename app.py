from flask import Flask, render_template
from flask.helpers import url_for
import config
from bd import db
from blueprint.gestion_cas.gestion_cas import routes


def create_app():
    app = Flask(__name__, template_folder='blueprint')
    app.config.from_object(config.DevelopmentConfig)
    app.register_blueprint(routes)
    compte = f'{app.config["DB_USERNAME"]}:{app.config["DB_PASSWORD"]}'
    serveur_bd = f'{app.config["DB_SERVEUR"]}/{app.config["DB_NAME"]}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"""mysql://{compte}@{serveur_bd}"""
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


@app.route('/')
def index():
    return 'Test'


if __name__ == '__main__':
    app.run(debug=True)
