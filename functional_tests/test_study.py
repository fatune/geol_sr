from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

    def test_user_begin_studying_for_the_1st_tim(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention Geology 
        self.assertIn('Geology', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Geology', header_text)

        # User is invited to login
        # user notices login link
        link = self.browser.find_element_by_link_text('Login')

        # user click login link and sees login page
        link.click()
        login_url = self.browser.current_url
        self.assertRegex(login_url, 'login')

        # user notices login input in inputs his login
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('selenium')

        # user notices pass input in inputs his pass
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('pass')
        password_field.send_keys(Keys.RETURN)

        # user notices that he's redirected to homem page
        time.sleep(2)
        #self.wait_for(self.assertEqual( self.browser.current_url, self.live_server_url))
        self.assertEqual( self.browser.current_url, self.live_server_url)

        # User is invited to follow a link to study a NE subject
        link = self.browser.find_element_by_link_text('Study NE')


        # User follows the link and notices that link has changed
        link.click()
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/study')

        # User reads a fancy introduction 
        text = self.browser.find_element_by_id('id_front_text').text
        self.assertIn('Welcome!', text)

        # User sees 'Show' button
        button = self.browser.find_element_by_id('id_button_show')

        # User hits enter and sees a first question map
        button.send_keys(Keys.ENTER)
        text = self.browser.find_element_by_id('id_front_text').text
        self.assertIn('First Question', text)

        # User clicks button and sees an answer to the first question map
        # and two buttons "Bad" and "Good"

        # User clicks "Bad" button and sees a first question map again

        # User clicks button and sees an answer to the first question map
        # and two buttons "Bad" and "Good"

        # Now User clicks "Good" button and sees second question map 

        # User clicks button and sees an answer to the first question map
        # and two buttons "Bad" and "Good"

        # Now User clicks "Good" button and sees third question with texts with blank words

        # User clicks button and sees and anwer to the third question

        # User clicks "Good" button and sees final screen with greetings
