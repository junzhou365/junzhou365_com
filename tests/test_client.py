import re
import unittest
from flask import url_for
from junzhou365 import create_app, db
from junzhou365.catalog.loginManager import User

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('home.showHome'))
        self.assertTrue(response.status_code == 200)

    def test_signup_and_login(self):
        response = self.client.post(url_for('catalog.signup'), data= {
            'username': '223',
            'password': '223',
            'verify':   '223',
        })
        self.assertTrue(response.status_code == 302)

        # log out
        response = self.client.get(url_for('catalog.logout'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)


