import os
import sys
import re
from django.core import mail
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

from sr.import_course import import_course_from_csv_similar_second_card

MAX_WAIT = 10

TEST_EMAIL = 'test@ex.com'
SUBJECT = 'Your login link for Superlists'

class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    def setUp(self):
    #    self.browser = webdriver.Firefox()
    #    staging_server = os.environ.get('STAGING_SERVER')
    #    if staging_server:
    #        self.live_server_url = 'http://' + staging_server
        if self.against_staging:
            reset_database(self.server_host)

        self.browser = webdriver.Firefox()

        import_course_from_csv_similar_second_card('./courses/tect_small.csv', 'Study NE')

    def tearDown(self):
        self.browser.quit()

    def login(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail('Could not find url in email body:\n%s' % email.body)
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)


    #def setUp(self):
    #    self.browser = webdriver.Firefox()
    #    staging_server = os.environ.get('STAGING_SERVER')
    #    if staging_server:
    #        self.live_server_url = 'http://' + staging_server
    #    #else: self.live_server_url = 'http://localhost:8000/'
    #    #self.live_server_url = self


    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
