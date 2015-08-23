from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

import sys
from os import path
import logging
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
sys.path.insert(0, path.dirname(path.abspath(__file__)))
sys.path.append('/vagrant/Projects/tushare') # tushare path

app = Flask(__name__, static_folder='static')
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from redirectToResume import home
    app.register_blueprint(home)

    from resume import resume
    app.register_blueprint(resume, url_prefix='/resume')

    from catalog import catalog
    app.register_blueprint(catalog, url_prefix='/catalog')

    from mystock import stock
    app.register_blueprint(stock, url_prefix='/stock')
    return app
