from flask import Blueprint, render_template, flash, request

routes_erreurs = Blueprint('gestion_erreurs', __name__,
                           template_folder='templates')


@routes_erreurs.app_errorhandler(404)
def page_not_found(e):
    flash("La page demandée n'existe pas", 'danger')
    return render_template('erreur.html', e=e), 404


@routes_erreurs.app_errorhandler(403)
def forbidden(e):
    flash("Vous n'avez pas les droits pour accéder à cette page", 'danger')
    return render_template('erreur.html', e=e), 403


@routes_erreurs.app_errorhandler(401)
def unauthorized(e):
    flash("Vous n'êtes pas autorisé à accéder à cette page", 'danger')
    return render_template('erreur.html', e=e), 401


@routes_erreurs.app_errorhandler(500)
def internal_server_error(e):
    flash("Une erreur interne est survenue", 'danger')
    return render_template('erreur.html', e=e), 500
