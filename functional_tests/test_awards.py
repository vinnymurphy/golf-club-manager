from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestAwards(FunctionalTest):

    def test_can_view_attendance_for_period(self):
        # Bob wants to check who is leading in attendance points
        self.login()
        self.browser.find_element_by_link_text('Attendance').click()

        # He sees the correct heading appear
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Attendance Points"
        ))

        # He fills in the range he cares about and submits
        self.replace_value_in_form('id_start', '01/01/2017')
        self.replace_value_in_form('id_end', '10/01/2017')
        self.browser.find_element_by_tag_name('button').click()

        # The results period is displayed and the table shows correct results
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_results_heading').text,
            "Results: 01 Jan 2017 - 01 Oct 2017"
        ))

        self.check_values_in_table(
            'id_results_table',
            '1 Abbott, Tony 9',
            'tr'
        )
        self.check_values_in_table(
            'id_results_table',
            '2 Fadden, Arthur 7',
            'tr'
        )

    def test_can_view_stableford_award_for_period(self):
        # Bob wants to check who is leading in attendance points
        self.login()
        self.browser.find_element_by_link_text('Stableford Award').click()

        # He sees the correct heading appear
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Stableford Award"
        ))

        # He fills in the range he cares about and submits
        self.replace_value_in_form('id_start', '01/01/2017')
        self.replace_value_in_form('id_end', '10/01/2017')
        self.browser.find_element_by_tag_name('button').click()

        # The results period is displayed and the table shows correct results
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_results_heading').text,
            "Results: 01 Jan 2017 - 01 Oct 2017"
        ))

        self.check_values_in_table(
            'id_results_table',
            '1 Fadden, Arthur 222',
            'tr'
        )
        self.check_values_in_table(
            'id_results_table',
            '2 Watson, Chris 212',
            'tr'
        )
        self.check_values_in_table(
            'id_results_table',
            '3 Howard, John 209',
            'tr'
        )
        self.check_values_in_table(
            'id_results_table',
            '4 Abbott, Tony 203',
            'tr'
        )
