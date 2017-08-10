from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import os
import time


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    fixtures = [
        'test_players.json',
        'test_gametypes.json',
        'test_grade.json',
        'test_user.json',
        'test_games.json'
        ]

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.refresh() # Prevents random errno 10054 error output
        self.browser.close()

    def check_values_in_table(self, table, data_text, val):
        table = self.browser.find_element_by_id(table)
        elements = table.find_elements_by_tag_name(val)
        self.assertIn(data_text, [element.text for element in elements])

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def login(self):
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('test')
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('test')
        inputbox.send_keys(Keys.ENTER)

    def replace_value_in_form(self, element_id, new_value):
        element = self.browser.find_element_by_id(element_id)
        element.clear()
        element.send_keys(new_value)

    def choose_dropdown_item(self, element_id, choice):
        dropdown = self.browser.find_element_by_id(element_id)
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == choice:
                option.click()
                break
