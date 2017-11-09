from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GameTest(FunctionalTest):

    def test_can_record_Stroke_game(self):
        # Bob has just finished playing a round of golf with the club and has
        # to get everyone's new handicap
        self.login()

        # He navigates to the Record a game page
        self.browser.find_element_by_link_text('Record a game').click()

        # He waits for the page to load and then starts filling in the form
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Record a game"
        ))

        self.replace_value_in_form('id_game_date', '07/29/2017')

        self.choose_dropdown_item('id_game_type', 'Stroke')

        self.replace_value_in_form('id_form-0-score', '74')
        self.replace_value_in_form('id_form-3-score', '72')
        self.replace_value_in_form('id_form-5-score', '70')
        self.replace_value_in_form('id_form-7-score', '69')
        self.replace_value_in_form('id_form-8-score', '0')

        self.browser.find_element_by_tag_name("button").click()

        # He notices the Players page then reloads and he can see that
        # the players scores have adjusted
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Players"
        ))

        self.check_values_in_table(
            "id_player_table",
            "Abbott, Tony 18.3 18 2017-07-29 0.3 Edit / Expand",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Chifley, Ben 18.5 18 2017-07-29 -0.5 Edit / Expand",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Curtin, John 40.0 40 2017-07-29 -1.0 Edit / Expand",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Dudd, Kevin 25.0 25 2017-07-29 -2.0 Edit / Expand",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Fadden, Arthur 7.0 7 None None Edit / Expand",
            "tr"
        )

    def test_can_record_Stableford_game(self):
        # Bob has just finished playing a round of golf with the club and has
        # to get everyone's new handicap
        self.login()

        # He navigates to the Record a game page
        self.browser.find_element_by_link_text('Record a game').click()

        # He waits for the page to load and then starts filling in the form
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Record a game"
        ))

        self.replace_value_in_form('id_game_date', '06/20/2017')

        self.choose_dropdown_item('id_game_type', 'Stableford')

        self.replace_value_in_form('id_form-0-score', '41')
        self.replace_value_in_form('id_form-3-score', '39')
        self.replace_value_in_form('id_form-5-score', '37')
        self.replace_value_in_form('id_form-7-score', '36')

        self.browser.find_element_by_tag_name("button").click()

        # He notices the Players page then reloads and he can see that
        # the players scores have adjusted
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Players"
        ))

        self.check_values_in_table(
            "id_player_table",
            "Abbott, Tony 16.0 16 2017-06-20 -2.0 Edit / Expand",
            "tr"
        )
        self.check_values_in_table("id_player_table",
            "Chifley, Ben 18.0 18 2017-06-20 -1.0 Edit / Expand",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Curtin, John 40.5 40 2017-06-20 -0.5 Edit / Expand",
            "tr"
        )
        self.check_values_in_table(
            "id_player_table",
            "Dudd, Kevin 27.3 27 2017-06-20 0.3 Edit / Expand",
            "tr"
        )

    def test_can_record_fun_match(self):
        # Bob has just finished playing a round of golf with the club and has
        # to get everyone's new handicap
        self.login()

        # He navigates to the Record a game page
        self.browser.find_element_by_link_text('Record a game').click()

        # He waits for the page to load and then starts filling in the form
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Record a game"
        ))

        self.replace_value_in_form('id_game_date', '09/27/2017')

        self.choose_dropdown_item('id_game_type', 'Fun match')

        self.replace_value_in_form('id_form-0-score', '41')

        self.browser.find_element_by_tag_name("button").click()

        # He notices the Players page then reloads and he can see that
        # the players scores have adjusted
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Players"
        ))

        self.check_values_in_table(
            "id_player_table",
            "Abbott, Tony 18.0 18 2017-09-27 None Edit / Expand",
            "tr"
        )

        # Bob wants to look at the list of games that Tony Abbott played
        self.browser.find_element_by_id('id_expand_28').click()

        # Tony's game history page loads up
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Tony Abbott"
        ))
        self.check_values_in_table(
            'id_expanded_player_table',
            '27 Sep 2017 Fun match None 1 Edit',
            'tr'
        )

    def test_can_view_game_history(self):
        # Bob can't remember if he recorded the game played on 30 July 2017,
        # so he loads up the website to check. He clicks the relevant link
        self.login()

        self.browser.find_element_by_link_text('Game History').click()

        # Page reloads to show Bob that he did record that game after all
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            'Games'
        ))

        list_items = self.browser.find_elements_by_tag_name('li')
        self.assertIn(
            '2017-07-30 - Stableford',
            [data.text for data in list_items]
        )

    def test_can_update_game(self):
        # Login and navigate to the game history page
        self.login()
        self.browser.find_element_by_link_text('Game History').click()
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            'Games'
        ))

        # Picks a game
        self.browser.find_element_by_link_text('2017-07-30 - Stableford').click()

        # The relevant game loads
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            '30 Jul 2017 - Stableford'
        ))

        # The correct values appear in the table
        self.check_values_in_table(
            'id_expand_game_table',
            'Howard, John 34 0.7 0.3 1 Edit',
            'tr'
        )
        self.check_values_in_table(
            'id_expand_game_table',
            'Fadden, Arthur 37 24.5 -0.5 1 Edit',
            'tr'
        )
        self.check_values_in_table(
            'id_expand_game_table',
            'Watson, Chris 39 24.5 -0.5 1 Edit',
            'tr'
        )
        self.check_values_in_table(
            'id_expand_game_table',
            'Abbott, Tony 36 24.5 -0.5 3 Edit',
            'tr'
        )

        # User realises they forgot to record someones score and decides
        # to update the game
        self.browser.find_element_by_link_text('Update Game').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Update game"
        ))

        self.replace_value_in_form('id_form-4-score', '42')
        self.replace_value_in_form('id_form-4-attendance', '4')
        self.browser.find_element_by_tag_name("button").click()

        # User is redirected back to the expanded game page
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            '30 Jul 2017 - Stableford'
        ))

        # The new values appear in the table
        self.check_values_in_table(
            'id_expand_game_table',
            'Curtin, John 42 41.0 -2.0 4 Edit',
            'tr'
        )
    
    def test_can_delete_game(self):
        # User realises they accidentally recorded the latest match as Stableford
        # instead of Stroke. They go to game history to try and delete it/roll it
        # back
        self.login()
        self.browser.find_element_by_link_text('Game History').click()
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            'Games'
        ))

        # Picks the incorrectly recorded game
        self.browser.find_element_by_link_text('2017-10-01 - Stableford').click()

        # The relevant game loads
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            '01 Oct 2017 - Stableford'
        ))

        # User selects delete option and a warning pops up to confirm they want
        # to delete the game
        self.browser.find_element_by_link_text('Delete Game').click()
        self.browser.switch_to_alert().accept()

        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            'Players'
        ))

        # The handicap change has been reversed on the player list
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            'Players'
        ))
        self.check_values_in_table(
            'id_player_table',
            'Abbott, Tony 17.5 18 None 0.5 Edit / Expand',
            'tr'
        )

        # User then confirms the game no longer appears on the game history page
        self.browser.find_element_by_link_text('Game History').click()
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element_by_id('id_page_heading').text,
            'Games'
        ))

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('01 Oct 2017 - Stableford', page_text)


class GameTypeTest(FunctionalTest):

    def test_can_view_game_types(self):
        # Bob wants to add a new game type called Stringball
        self.login()

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
        self.login()

        # He looks at the available content and eventually clicks the Settings
        # button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob clicks the button to add a new game type. He is prompted to log in
        self.browser.find_element_by_link_text('Add New Game Type').click()

        # Upon successfully logging in he sees that the correct page has loaded
        # and starts filling in the rules
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Add New Game Type"
        ))

        self.replace_value_in_form('id_name', 'Stringball')
        self.replace_value_in_form('id_level_4', '10')
        self.replace_value_in_form('id_level_4_result', '0.3')
        self.replace_value_in_form('id_level_3_min', '11')
        self.replace_value_in_form('id_level_3_max', '12')
        self.replace_value_in_form('id_level_3_result', '-0.5')
        self.replace_value_in_form('id_level_2_min', '13')
        self.replace_value_in_form('id_level_2_max', '14')
        self.replace_value_in_form('id_level_2_result', '-1.0')
        self.replace_value_in_form('id_level_1', '15')
        self.replace_value_in_form('id_level_1_result', '-2')
        self.browser.find_element_by_tag_name("button").click()

        # The page reloads and Bob sees his game type in the list
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Settings"
        ))
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stringball', [types.text for types in game_types])

    def test_can_edit_game_type(self):
        # Bob wants to rename the Stableford game type to Stringball
        self.login()

        # He clicks the settings button
        self.browser.find_element_by_link_text('Settings').click()

        # Bob clicks the Edit button next to Stableford.
        # He is prompted to log in
        self.browser.find_element_by_id('edit-Stableford').click()

        # Upon successfully logging in he sees that the correct page has loaded
        # and renames the game type
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Edit Game Type"
        ))

        self.replace_value_in_form('id_name', 'Stringball')
        self.browser.find_element_by_tag_name('button').click()

        # The page reloads and Bob sees his game type in the list
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Settings"
        ))
        game_types = self.browser.find_elements_by_class_name(
            'settings-list-title')
        self.assertIn('Stringball', [types.text for types in game_types])
        self.assertNotIn('Stableford', [types.text for types in game_types])
