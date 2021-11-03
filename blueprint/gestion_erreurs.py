from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from blueprint.comptes.comptes import Comptes
from bd import db

routes_erreurs = Blueprint('gestion_erreurs', __name__)


@routes_erreurs.app_errorhandler(404)
def page_not_found(e):
    return '404'


@routes_erreurs.app_errorhandler(500)
def internal_server_error(e):
    return '500'


@routes_erreurs.app_errorhandler(403)
def forbidden(e):
    return '403'


@routes_erreurs.app_errorhandler(401)
def unauthorized(e):
    return '401'


@routes_erreurs.app_errorhandler(400)
def bad_request(e):
    return '400'


@routes_erreurs.app_errorhandler(405)
def method_not_allowed(e):
    return '405'


@routes_erreurs.app_errorhandler(503)
def service_unavailable(e):
    return '503'
