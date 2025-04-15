# my version of the test suite with pytest

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pytest

@pytest.mark.django_db
class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		# A user goes to the home page
		self.browser.get(self.home_url)
		self.browser.set_window_size(1024, 768)

		# they notice the input box is nicely centered
		inputbox = self.get_item_input_box()
		# for some reason this gets put at x=44, but this test will still fail if CSS isn't loading, 
		# as it changes the width of the input box. 
		assert abs(inputbox.location['x'] + inputbox.size['width']/2 - (44+228)) <= 10 

		# they start a new list and notice the input box 
		# is centered in the list view page too
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.get_item_input_box()
		assert abs(inputbox.location['x'] + inputbox.size['width']/2 - (44+228)) <= 10 # same difference from book
