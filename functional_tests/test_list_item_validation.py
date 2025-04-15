# my version of the test suite with pytest

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pytest

@pytest.mark.django_db
class ItemValidationTest(FunctionalTest):
	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit 
		# an empty list item. She hits enter on the empty input box. 
		self.browser.get(self.home_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# The home page refreshes, and there is an error message saying
		# that the list cannot be blank. 
		def check_empty_error():
			assert self.browser.find_element(By.CSS_SELECTOR, ".has_error").text == "You can't have an empty list item"
		self.wait_for(check_empty_error)

		# She tries again with some text for this item, which now works. 
		self.get_item_input_box().send_keys("Buy milk")
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy milk")

		# For some reason, she decides to submit a second empty list item. 
		self.get_item_input_box().send_keys(Keys.ENTER)

		# She recieves a similar warning on the list page. 
		self.wait_for(check_empty_error)

		# And she can correct it by filling some text in. 
		self.get_item_input_box().send_keys("Make tea")
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy milk")
		self.wait_for_row_in_list_table("2: Make tea")