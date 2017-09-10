from selenium import webdriver
import unittest
import threading
import re
from app import create_app, db
from app.models import Role, User, Post
import time

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Firefox()
        except:
            pass
        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getlogger('werkzeug')
            logger.setLevel('ERROR')

            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            admin_role = Role.query.filter_by(permission = 0xff).first()
            admin = User(email = 'jo@qq.com', username = 'cll', password = '144',
                         role = admin_role, confirmed = True)
            db.session.add(admin)
            db.session.commit()

            threading.Thread(target = cls.app.run).start()
            time.sleep(1)

    @classmethod
    def tearDowmClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not aviliable')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello, \s+cll', self.client.page.source))

        self.client.find_element_by_link_text('sign in').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        self.client.find_element_by_name('email').send_keys('jo@qq.com')
        self.client.find_element_by_name('password').send_keys('144')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+cll', self.client.page_source))

        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>cll</h1>' in self.client.page_source)
