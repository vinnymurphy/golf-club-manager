from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewGameTest(FunctionalTest):

    # def test_can_record_game(self):
    #     # Bob has just finished playing a round of golf with the club and has
    #     # to get everyone's new handicap
    #     self. browser.get(self.live_server_url)
    #
    #     # He navigates to the Record a game page
    #     self.browser.find_element_by_link_text('Record a game').click()
    #
    #     # He starts filling in the form
    #

    def test_can_create_new_game_type(self):
        # Bob wants to add a new game type called Stringball
        self.browser.get(self.live_server_url)

        # He looks at the available content and eventually clicks the Settings
        # button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob is then presented with the existing game types
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stableford', [types.text for types in game_types])
        self.assertIn('Stroke', [types.text for types in game_types])
        self.assertNotIn('Stringball', [types.text for types in game_types])

        # Confident that the game type he desires is not listed, he clicks
        # the button to add a new game type. He is prompted to log in
        self.browser.find_element_by_link_text('Add New Game Type').click()

        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('test')
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('test')
        inputbox.send_keys(Keys.ENTER)

        # Upon successfully logging in he sees that the correct page has loaded
        # and starts filling in the rules
        self.wait_for(
            lambda: self.browser.find_element_by_id('page-heading')
        )

        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('Stringball')
        inputbox = self.browser.find_element_by_id('id_level_4')
        inputbox.send_keys('10')
        inputbox = self.browser.find_element_by_id('id_level_4_result')
        inputbox.send_keys('0.3')
        inputbox = self.browser.find_element_by_id('id_level_3_min')
        inputbox.send_keys('11')
        inputbox = self.browser.find_element_by_id('id_level_3_max')
        inputbox.send_keys('12')
        inputbox = self.browser.find_element_by_id('id_level_3_result')
        inputbox.send_keys('-0.5')
        inputbox = self.browser.find_element_by_id('id_level_2_min')
        inputbox.send_keys('13')
        inputbox = self.browser.find_element_by_id('id_level_2_max')
        inputbox.send_keys('14')
        inputbox = self.browser.find_element_by_id('id_level_2_result')
        inputbox.send_keys('-1.0')
        inputbox = self.browser.find_element_by_id('id_level_1')
        inputbox.send_keys('15')
        inputbox = self.browser.find_element_by_id('id_level_1_result')
        inputbox.send_keys('-2')
        inputbox.send_keys(Keys.ENTER)

        # The page reloads and Bob sees his game type in the list
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Settings"
        ))
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stringball', [types.text for types in game_types])
