from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PlayersTest(FunctionalTest):

    def test_can_add_player(self):
        # Bob has a visitor coming to play golf for a couple of weeks and would
        # like to add them to the system. He loads up the website and clicks
        # the link to add a players
        self.login()

        self.browser.find_element_by_link_text('Add New Player').click()

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Add New Player"
        ))

        self.replace_value_in_form('id_first_name', 'Barack')
        self.replace_value_in_form('id_last_name', 'Obama')
        self.replace_value_in_form('id_handicap', '1')
        self.browser.find_element_by_tag_name("button").click()

        # Bob checks to see the visitor is in the active player list
        self.check_values_in_table(
            'id_player_table',
            'Obama, Barack',
            'td'
        )

    def test_can_mark_player_inactive(self):
        # Bob wants to review all activate players, as he can't remember if he
        # already updated the system to have Earle Page as inactive. He loads
        # up the website
        self.login()

        # He's immediately presented with the active player list and their
        # scores
        self.browser.find_element_by_id('id_player_table')

        # He sees that Earle is still listed, and clicks the edit button
        self.check_values_in_table(
            'id_player_table',
            'Page, Earle',
            'td'
        )

        self.browser.find_element_by_id('id_player_11').click()

        # He's presented with the Edit Player screen pre-populated with Earle's
        # details and sees that the Active box is ticked
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Edit Player"
        ))

        checkbox = self.browser.find_element_by_id('id_active')
        self.assertTrue(checkbox.is_selected())

        # Bob unticks the checkbox and clicks the Update Player button
        checkbox.click()
        self.browser.find_element_by_tag_name("button").click()

        # The page loads and he's back looking at the active player table and
        # confirms he can no longer see Earle. He clicks the link to view
        # inactive players
        table = self.browser.find_element_by_id('id_player_table')
        columns = table.find_elements_by_tag_name('td')
        self.assertNotIn(
            'Page, Earle', [column.text for column in columns])

        self.browser.find_element_by_link_text('Inactive Players').click()
        self.check_values_in_table(
            'id_inactive_player_table',
            'Page, Earle',
            'td'
        )

    def test_can_expand_player(self):
        self.login()

        # Bob wants to look at the list of games that Tony Abbott played
        self.browser.find_element_by_id('id_expand_28').click()

        # Tony's game history page loads up
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Tony Abbott"
        ))
        self.check_values_in_table(
            'id_expanded_player_table',
            '30 Jul 2017 Stableford 36',
            'tr'
        )
