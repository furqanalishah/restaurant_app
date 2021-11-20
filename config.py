import logging
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class PaginationConfig:
    DEFAULT_ITEMS_PER_PAGE = 10
    MAX_ITEMS_PER_PAGE = 50


class EncryptionConfig:
    SALT_LENGTH = 32
    DERIVATION_ROUNDS = 100000
    BLOCK_SIZE = 16
    KEY_SIZE = 32
    SECRET = "nw2FrNshF"


class POSTGRESConfig:
    POSTGRES_PARAMS = {
        "POSTGRES_USER": os.environ.get("POSTGRES_USER", "syed"),
        "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD", "syedfurqan"),
        "POSTGRES_HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "POSTGRES_PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "POSTGRES_DATABASE": os.environ.get("POSTGRES_DATABASE", "restaurant_app")
    }

    POSTGRES_DB_URL = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}".format(
        **POSTGRES_PARAMS
    )


class SQLAlchemyConfig:
    SQLALCHEMY_DATABASE_URI = POSTGRESConfig.POSTGRES_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get("SQLALCHEMY_POOL_RECYCLE", "400"))
    SQLALCHEMY_POOL_TIMEOUT = int(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", "450"))
    SQLALCHEMY_POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", "5"))
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", "0"))
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
        "pool_timeout": SQLALCHEMY_POOL_TIMEOUT,
        "pool_size": SQLALCHEMY_POOL_SIZE,
        "max_overflow": SQLALCHEMY_MAX_OVERFLOW
    }


class MailConfig:
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "mefurqan123@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "zdtttemvjaelapnq")

    # mail accounts
    MAIL_DEFAULT_SENDER = "mefurqan123@gmail.com"


class FlaskConfig:
    __LOGGING_LEVEL_MAPPER = {
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    try:
        LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG")
        LOGGING_LEVEL_MAPPED = __LOGGING_LEVEL_MAPPER[LOGGING_LEVEL]
    except KeyError:
        raise ValueError(f"LOGGING_LEVEL should be one of {list(__LOGGING_LEVEL_MAPPER.keys())}")

    SECRET_KEY = os.environ.get("SECRET_KEY", "my_precious_aws")
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAX_CONTENT_LENGTH = 2048 * 2048


class FlaskDevelopmentConfig(FlaskConfig, SQLAlchemyConfig, MailConfig):
    # Flask Configs
    DEBUG = True
    USE_SSL = os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Port is not a flask env variable but is used in a custom logic to set the port for the flask server
    PORT = 8081


flask_config = {
    "development": FlaskDevelopmentConfig,
    "default": FlaskDevelopmentConfig,
}
