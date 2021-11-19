""" Module des configurations. """


class Config():
    """ Modèle de configuration de base. """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    DB_NAME = ""
    DB_USERNAME = ""
    DB_PASSWORD = ""
    HOST = ""

    IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False

    DEFAULT_LOCALE = "fr_CA"

    HOST = "0.0.0.0"


class DevelopmentConfig(Config):
    """ Configuration de développement. """
    DEBUG = True

    DB_NAME = "gestion_covid"
    DB_USERNAME = "root"
    DB_PASSWORD = "mysql"
    DB_SERVEUR = "localhost"


class TestingConfig(Config):
    """ Configuration de test. """
    TESTING = True

    DB_NAME = "gestion_covid"
    DB_USERNAME = "ubuntuserver"
    DB_PASSWORD = ""
    DB_SERVEUR = "localhost"
