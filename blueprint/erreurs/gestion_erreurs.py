from flask import Blueprint, render_template, flash, request, session

routes_erreurs = Blueprint('gestion_erreurs', __name__,
                           template_folder='templates')


@routes_erreurs.app_errorhandler(404)
def page_not_found(e):
    flash("La page demandée n'existe pas: " +
          request.full_path.replace('?', ''), 'danger')
    return render_template('erreur.html', e=e), 404


@routes_erreurs.app_errorhandler(403)
def forbidden(e):
    flash("Vous devez être administrateur pour accéder à cette page: " +
          (session.get('url') or ''), 'danger')
    return render_template('erreur.html', e=e), 403


@routes_erreurs.app_errorhandler(401)
def unauthorized(e):
    flash("Vous devez être authentifié pour accéder à cette page: " +
          session.get('url'), 'danger')
    return render_template('erreur.html', e=e), 401


@routes_erreurs.app_errorhandler(500)
def internal_server_error(e):
    flash("Une erreur interne est survenue", 'danger')
    return render_template('erreur.html', e=e), 500
