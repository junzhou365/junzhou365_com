import unittest
from factory import create_app, db
from flask import url_for
from catalog.catalog_models import Category, Item, Image
import logging

class FlaskViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

        # signup a new user
        response = self.client.post(url_for('catalog.signup'), data= {
            'username': '123',
            'password': '123',
            'verify':   '123',
        })
        self.assertTrue(response.status_code == 302)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('home.showHome'))
        self.assertTrue(response.status_code == 200)

    def test_catalog_home(self):
        response = self.client.get(url_for('catalog.renderHomePage'))
        self.assertTrue(response.status_code == 200)

    def test_new_category(self):
        response = self.client.get(url_for('catalog.newCategory'))
        self.assertTrue(response.status_code == 200)

        response = self.client.post(url_for('catalog.newCategory'), data={
            'category_name' : 'tess', 
        }, follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        data = response.get_data(as_text=True)
        self.assertTrue("tess" in data)

        response = self.client.post(url_for('catalog.newCategory'), data={
            'category_name' : 'tess', 
        }, follow_redirects=True)
        #logging.error(response.status)
        self.assertTrue(response.status_code == 200)
        data = response.get_data(as_text=True)
        self.assertTrue("Category already exists" in data)

        response = self.client.post(url_for('catalog.newCategory'), data={
            'category_name' : '', 
        }, follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        data = response.get_data(as_text=True)
        self.assertTrue("Empty Category Name" in data)

        Category.delete_by_id(Category.get_by_name('tess').id)

    def test_edit_category(self):
        category = Category.store('Wuki')
        response = self.client.get(url_for('catalog.editCategory', category_id=category.id))
        self.assertTrue(response.status_code == 200)

        response = self.client.post(url_for('catalog.editCategory', category_id=category.id), data= {
            'category_name' : 'tess', 
        }, follow_redirects=True)
        logging.error(response.status)
        self.assertTrue(response.status_code == 200)
        data = response.get_data(as_text=True)
        self.assertTrue("tess" in data)

    def test_delete_category(self):
        pass
        


        
        


