import re
import unittest
from flask import url_for
from factory import create_app, db
from catalog.loginManager import User
import logging

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

    def test_signup_and_login(self):
        response = self.client.post(url_for('catalog.signup'), data= {
            'username': '223',
            'password': '223',
            'verify':   '223',
        })
        self.assertTrue(response.status_code == 302)

        response = self.client.get(url_for('catalog.renderHomePage'))
        self.assertTrue("Signed in as 223" in response.get_data(as_text=True))

        # log out
        response = self.client.get(url_for('catalog.logout'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)


        # user exists
        response = self.client.post(url_for('catalog.signup'), data= {
            'username': '223',
            'password': '223',
            'verify':   '223',
        })
        self.assertTrue(response.status_code == 200)
        self.assertTrue("User already exists" in response.get_data(as_text=True))

        # passwords mismatch
        response = self.client.post(url_for('catalog.signup'), data= {
            'username': '233',
            'password': '233',
            'verify':   '223',
        })
        self.assertTrue(response.status_code == 200)
        self.assertTrue("Passwords Mismatch" in response.get_data(as_text=True))

        # log in
        response = self.client.get(url_for('catalog.login'))
        self.assertTrue(response.status_code == 200)

        response = self.client.post(url_for('catalog.login'),  data= {
            'username' : '223',
            'password' : '233',
        }, follow_redirects=True)
        self.assertTrue("Invalid Login" in response.get_data(as_text=True))

        response = self.client.post(url_for('catalog.login'),  data= {
            'username' : '223',
            'password' : '233',
        }, follow_redirects=True)
        self.assertTrue("Invalid Login" in response.get_data(as_text=True))

        response = self.client.post(url_for('catalog.login'),  data= {
            'username' : '223',
            'password' : '223',
        }, follow_redirects=True)
        self.assertTrue("Signed in as 223" in response.get_data(as_text=True))
