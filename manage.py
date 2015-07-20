#!/usr/bin/env python
import os
import sys

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, source=['/vagrant/Projects/junzhou365/catalog/', '/vagrant/Projects/junzhou365/home/'])
    COV.start()

from factory import create_app
from flask.ext.script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

@manager.command
def init_db():
    """Initialize database"""
    from factory import db, app
    app = create_app('default')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    from catalog.init_db import database_init
    x = database_init.fill_examples
    x()
    app_context.pop()

@manager.command
def drop_db():
    """Initialize database"""
    from factory import db, app
    app = create_app('default')
    app_context = app.app_context()
    app_context.push()
    db.drop_all()
    app_context.pop()

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

if __name__ == '__main__':
    manager.run()
