import os
from dotenv import dotenv_values

basedir = os.path.abspath(os.path.dirname(__file__))
env_config = dotenv_values(os.path.join(basedir, ".env"))

DATABASE_URL = f"postgresql://{env_config['DB_USERNAME']}:{env_config['DB_PASSWORD']}@{env_config['DB_HOST']}/{env_config['DB_NAME']}"


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = env_config["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
