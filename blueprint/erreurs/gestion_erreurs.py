""" Module de gestion des erreurs. """
from flask import Blueprint, render_template, flash, request, session

routes_erreurs = Blueprint('gestion_erreurs', __name__,
                           template_folder='templates')


@routes_erreurs.app_errorhandler(404)
def page_not_found(error):
    """ Route de la page d'erreur 404.

    Returns:
        Render_template: La page d'erreur 404
    """
    flash("La page demandée n'existe pas: " +
          request.full_path.replace('?', ''), 'danger')
    return render_template('erreur.html', e=error), 404


@routes_erreurs.app_errorhandler(403)
def forbidden(error):
    """ Route de la page d'erreur 403.

    Returns:
        Render_template: La page d'erreur 403
    """
    flash("Vous devez être administrateur pour accéder à cette page: " +
          (session.get('url') or ''), 'danger')
    return render_template('erreur.html', e=error), 403


@routes_erreurs.app_errorhandler(401)
def unauthorized(error):
    """ Route de la page d'erreur 401.

    Returns:
        Render_template: La page d'erreur 401
    """
    flash("Vous devez être authentifié pour accéder à cette page: " +
          session.get('url'), 'danger')
    return render_template('erreur.html', e=error), 401


@routes_erreurs.app_errorhandler(500)
def internal_server_error(error):
    """ Route de la page d'erreur 500.

    Returns:
        Render_template: La page d'erreur 500
    """
    flash("Une erreur interne est survenue", 'danger')
    return render_template('erreur.html', e=error), 500
