class Config():
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    DB_NAME = ""
    DB_USERNAME = ""
    DB_PASSWORD = ""
    HOST = ""

    IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True

    DEFAULT_LOCALE = "fr_CA"

    HOST = "0.0.0.0"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "gestion_covid"
    DB_USERNAME = "root"
    DB_PASSWORD = "mysql"
    DB_SERVEUR = "localhost"

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "gestion_covid"
    DB_USERNAME = "ubuntuserver"
    DB_PASSWORD = ""
    DB_SERVEUR = "localhost"

    SESSION_COOKIE_SECURE = False
