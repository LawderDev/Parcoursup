import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuration de la base de données SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/database.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Autres configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')