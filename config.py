class Config(object):
    DEBUG = False

    DB_NAME = 'db_example'
    DB_USERNAME = 'example'
    DB_PASSWORD = 'example123'
    
    UPLOAD_PATH = 'src/assets/data/'

    ALLOWED_DOMAINS = ["http://localhost:4200","http://27.4.230.200:4200"]

class ProductionConfig(Config):
    DB_NAME = 'db_prod'
    DB_USERNAME = 'prod'
    DB_PASSWORD = 'prod123'

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = 'db_dev'
    DB_USERNAME = 'dev'
    DB_PASSWORD = 'dev123'