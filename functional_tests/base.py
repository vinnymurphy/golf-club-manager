from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import time


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    fixtures = [
        'test_players.json',
        'test_gametypes.json',
        'test_grade.json',
        'test_user.json'
        ]

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.refresh() # Prevents random errno 10054 error output
        self.browser.close()

    def check_values_in_player_table(self, data_text):
        table = self.browser.find_element_by_id("id_player_table")
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(data_text, [row.text for row in rows])


    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
