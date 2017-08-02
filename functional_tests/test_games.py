from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GameTest(FunctionalTest):

    def test_can_record_Stroke_game(self):
        # Bob has just finished playing a round of golf with the club and has
        # to get everyone's new handicap
        self.browser.get(self.live_server_url)

        # He navigates to the Record a game page
        self.browser.find_element_by_link_text('Record a game').click()

        # It makes him log in
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('test')
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('test')
        inputbox.send_keys(Keys.ENTER)

        # He waits for the page to load and then starts filling in the form
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Record a game"
        ))

        datebox = self.browser.find_element_by_id('id_game_date')
        datebox.send_keys("07/29/2017")

        dropdown = self.browser.find_element_by_id('id_game_type')
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == "Stroke":
                option.click()
                break

        scorebox = self.browser.find_element_by_id('id_form-0-score')
        scorebox.send_keys('74')
        scorebox = self.browser.find_element_by_id('id_form-3-score')
        scorebox.send_keys('72')
        scorebox = self.browser.find_element_by_id('id_form-5-score')
        scorebox.send_keys('70')
        scorebox = self.browser.find_element_by_id('id_form-7-score')
        scorebox.send_keys('69')

        self.browser.find_element_by_tag_name("button").click()

        # He notices the Players page then reloads and he can see that
        # the players scores have adjusted
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Players"
        ))

        self.check_values_in_player_table("Abbott, Tony - Edit 18.3 18 2017-07-29 0.3")
        self.check_values_in_player_table("Chifley, Ben - Edit 18.5 18 2017-07-29 -0.5")
        self.check_values_in_player_table("Curtin, John - Edit 40.0 40 2017-07-29 -1.0")
        self.check_values_in_player_table("Dudd, Kevin - Edit 25.0 25 2017-07-29 -2.0")

    def test_can_record_Stableford_game(self):
        # Bob has just finished playing a round of golf with the club and has
        # to get everyone's new handicap
        self.browser.get(self.live_server_url)

        # He navigates to the Record a game page
        self.browser.find_element_by_link_text('Record a game').click()

        # It makes him log in
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('test')
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('test')
        inputbox.send_keys(Keys.ENTER)

        # He waits for the page to load and then starts filling in the form
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Record a game"
        ))

        datebox = self.browser.find_element_by_id('id_game_date')
        datebox.send_keys("06/20/2017")

        dropdown = self.browser.find_element_by_id('id_game_type')
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == "Stableford":
                option.click()
                break

        scorebox = self.browser.find_element_by_id('id_form-0-score')
        scorebox.send_keys('41')
        scorebox = self.browser.find_element_by_id('id_form-3-score')
        scorebox.send_keys('39')
        scorebox = self.browser.find_element_by_id('id_form-5-score')
        scorebox.send_keys('37')
        scorebox = self.browser.find_element_by_id('id_form-7-score')
        scorebox.send_keys('36')

        self.browser.find_element_by_tag_name("button").click()

        # He notices the Players page then reloads and he can see that
        # the players scores have adjusted
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Players"
        ))

        self.check_values_in_player_table("Abbott, Tony - Edit 16.0 16 2017-06-20 -2.0")
        self.check_values_in_player_table("Chifley, Ben - Edit 18.0 18 2017-06-20 -1.0")
        self.check_values_in_player_table("Curtin, John - Edit 40.5 40 2017-06-20 -0.5")
        self.check_values_in_player_table("Dudd, Kevin - Edit 27.3 27 2017-06-20 0.3")


class GameTypeTest(FunctionalTest):

    def test_can_view_game_types(self):
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

    def test_can_create_new_game_type(self):
        # Bob wants to add a new game type called Stringball
        self.browser.get(self.live_server_url)

        # He looks at the available content and eventually clicks the Settings
        # button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob clicks the button to add a new game type. He is prompted to log in
        self.browser.find_element_by_link_text('Add New Game Type').click()

        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('test')
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('test')
        inputbox.send_keys(Keys.ENTER)

        # Upon successfully logging in he sees that the correct page has loaded
        # and starts filling in the rules
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Add New Game Type"
        ))

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

    def test_can_edit_game_type(self):
        # Bob wants to add a new game type called Stringball
        self.browser.get(self.live_server_url)

        # He looks at the available content and eventually clicks the Settings
        # button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob clicks the button to add a new game type. He is prompted to log in
        self.browser.find_element_by_id('edit-Stableford').click()

        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('test')
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('test')
        inputbox.send_keys(Keys.ENTER)

        # Upon successfully logging in he sees that the correct page has loaded
        # and starts filling in the rules
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Edit Game Type"
        ))

        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.clear()
        inputbox.send_keys('Stringball')
        inputbox.send_keys(Keys.ENTER)

        # The page reloads and Bob sees his game type in the list
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('page-heading').text,
            "Settings"
        ))
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stringball', [types.text for types in game_types])
