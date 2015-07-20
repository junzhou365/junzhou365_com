from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
sys.path.insert(0, path.dirname(path.abspath(__file__)))

app = Flask(__name__, static_folder='home/static')
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    from catalog import catalog
    app.register_blueprint(catalog, url_prefix='/catalog')

    return app

