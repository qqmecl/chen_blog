# -*- coding:utf-8 -*-
import unittest
from app import create_app, db
from app.models import User, Role
import re
from flask import url_for

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies = True)

    def tearDowm(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('光临' in response.get_data(as_text = True))

    def test_register_and_login(self):
        response = self.client.post(url_for('auth.register'), data = {
                'email': 'jo@example.com',
                'username': 'cl',
                'password': 144,
                'password2': 144})
        self.assertTrue(response.status_code == 302)

        response = self.client.post(url_for('auth.login'), data = {
                'email': 'jo@example.com',
                'password': 144}, follow_redirects = True)
        data = response.get_data(as_text = True)
        self.assertTrue(re.search('欢迎cl的到来', data))
        self.assertTrue('You have not confirmed' in data)

        user = User.query.filter_by(email = 'jo@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token = token), follow_redirects = True)
        data = response.get_data(as_text = True)
        self.assertTrue('You have confirmed your account' in data)

        response = self.client.get(url_for('auth.logout'), follow_redirects = True)
        data = response.get_data(as_text = True)
        self.assertTrue('You have been logged out' in data)
