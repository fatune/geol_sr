from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_user_begin_studying_for_the_1st_tim(self):
        # User visits homepage
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention Geology 
        self.assertIn('Geology', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Geology', header_text)

        # User is invited to follow a link to study a NE subject
        #link = self.browser.find_element_by_id('id_link_to_study')
        link = self.browser.find_element_by_link_text('Study NE')


        # User follows the link and notices that link has changed
        link.click()
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/study')

        # User reads a fancy introduction 

        # User hits enter and sees a first question map

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
