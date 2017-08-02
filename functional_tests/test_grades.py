from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GradesTest(FunctionalTest):

    def test_can_view_grades(self):
        # Bob wants to look who falls within the current 3 grades ahead of
        # one of their competitive GameScore
        self.browser.get(self.live_server_url)

        # He clicks the Grades button in the navigation bar
        self.browser.find_element_by_link_text('Grades').click()

        # Three tables appear on his page
        self.check_values_in_table(
            'id_grade_table_A',
            'Abbott, Tony',
            'td'
        )
        self.check_values_in_table(
            'id_grade_table_B',
            'Hughes, Billy',
            'td'
        )
        self.check_values_in_table(
            'id_grade_table_C',
            'Bruce, Stanley',
            'td'
        )

    def test_can_modify_grades(self):
        # Bob has to change the grading system as too many people are falling
        # within Grade A
        self.browser.get(self.live_server_url)

        # He navigates to settings and then to configure grades
        self.browser.find_element_by_link_text('Grades').click()
        self.browser.find_element_by_link_text('Configure Grades').click()

        # He changes some grades
        self.replace_value_in_form('id_grade_a_max', '30')
        self.replace_value_in_form('id_grade_b_min', '31')
        self.browser.find_element_by_tag_name("button").click()

        # He sees the table has updated correctly
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Grades"
        ))
        self.check_values_in_table(
            'id_grade_table_A',
            'Hughes, Billy',
            'td'
        )

    def test_can_use_4_grades(self):
        # Bob has to change the grading system as too many people are falling
        # within Grade A
        self.browser.get(self.live_server_url)

        # He navigates to settings and then to configure grades
        self.browser.find_element_by_link_text('Grades').click()
        self.browser.find_element_by_link_text('Configure Grades').click()

        # He changes to 4 grades
        self.choose_dropdown_item('id_grade_use', '4 grades')

        # He inputs the new grades
        self.replace_value_in_form('id_grade_a_min', '0')
        self.replace_value_in_form('id_grade_a_max', '20')
        self.replace_value_in_form('id_grade_b_min', '21')
        self.replace_value_in_form('id_grade_b_max', '29')
        self.replace_value_in_form('id_grade_c_min', '30')
        self.replace_value_in_form('id_grade_c_max', '36')
        self.replace_value_in_form('id_grade_d_min', '37')
        self.replace_value_in_form('id_grade_d_max', '46')
        self.browser.find_element_by_tag_name("button").click()

        # He sees the table has updated correctly
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Grades"
        ))

        self.check_values_in_table(
            'id_grade_table_B',
            'Cook, Joseph',
            'td'
        )
        self.check_values_in_table(
            'id_grade_table_C',
            'Scullin, James',
            'td'
        )
        self.check_values_in_table(
            'id_grade_table_D',
            'Bruce, Stanley',
            'td'
        )

    def test_can_use_5_grades(self):
        # Bob has to change the grading system as too many people are falling
        # within Grade A
        self.browser.get(self.live_server_url)

        # He navigates to settings and then to configure grades
        self.browser.find_element_by_link_text('Grades').click()
        self.browser.find_element_by_link_text('Configure Grades').click()

        # He changes to 4 grades
        self.choose_dropdown_item('id_grade_use', '5 grades')

        # He inputs the new grades
        self.replace_value_in_form('id_grade_a_min', '0')
        self.replace_value_in_form('id_grade_a_max', '14')
        self.replace_value_in_form('id_grade_b_min', '15')
        self.replace_value_in_form('id_grade_b_max', '23')
        self.replace_value_in_form('id_grade_c_min', '24')
        self.replace_value_in_form('id_grade_c_max', '33')
        self.replace_value_in_form('id_grade_d_min', '34')
        self.replace_value_in_form('id_grade_d_max', '40')
        self.replace_value_in_form('id_grade_e_min', '41')
        self.replace_value_in_form('id_grade_e_max', '45')
        self.browser.find_element_by_tag_name("button").click()

        # He sees the table has updated correctly
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_page_heading').text,
            "Grades"
        ))

        # Five tables appear on his page, so he checks who
        self.check_values_in_table(
            'id_grade_table_B',
            'Abbott, Tony',
            'td'
        )
        self.check_values_in_table(
            'id_grade_table_C',
            'Gillard, Julia',
            'td'
        )
        self.check_values_in_table(
            'id_grade_table_D',
            'Whitlam, Gough',
            'td'
        )
        self.check_values_in_table(
            'id_grade_table_E',
            'Keating, Paul',
            'td'
        )
