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

		# the broswer intercepts the request and does not load the 
		# list page
		def check_for_css_selector(selector):
			return self.browser.find_element(By.CSS_SELECTOR, selector)
		self.wait_for(check_for_css_selector, "#id_text:invalid")

		# she starts typing some text for the list item and the error disappears
		self.get_item_input_box().send_keys("Buy milk")
		self.wait_for(check_for_css_selector, "#id_text:valid")

		# and she can submit it successfully
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy milk")

		# For some reason, she decides to submit a second empty list item. 
		self.get_item_input_box().send_keys(Keys.ENTER)

		# again, the broswer will not comply
		self.wait_for_row_in_list_table("1: Buy milk")
		self.wait_for(check_for_css_selector, "#id_text:invalid")

		# And she can correct it by filling some text in. 
		self.get_item_input_box().send_keys("Make tea")
		self.wait_for(check_for_css_selector, "#id_text:valid")
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy milk")
		self.wait_for_row_in_list_table("2: Make tea")

	def test_cannot_add_duplicate_items(self):
		# Edith goes to the home page and starts a new list
		self.browser.get(self.home_url)
		self.get_item_input_box().send_keys("Buy wellies")
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table("1: Buy wellies")

		# She accidentally tries to enter a duplicate item
		self.get_item_input_box().send_keys("Buy wellies")
		self.get_item_input_box().send_keys(Keys.ENTER)

		# She sees a helpful error message
		def check_duplicate_item_error():
			assert self.browser.find_element(By.CSS_SELECTOR, ".has-error").text == \
				"You've already got this in your list"
		self.wait_for(check_duplicate_item_error)
