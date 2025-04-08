# my version of the test suite with pytest

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pytest
import re

@pytest.mark.django_db
class NewVisitorTest(FunctionalTest):
	# NOTE : live_server fixture runs a separate test server, then cleans up (equivalent of django.test.LiveServerTestCase)
	def test_can_start_a_list_for_one_user(self):

		# A user has heard about a new to-do app. They open the homepage
		self.browser.get(self.home_url)

		# and see that the page mentions to-do lists in its title
		assert "To-Do" in self.browser.title
		header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
		assert "To-Do" in header_text

		# The user is invited to enter a to-do list item
		inputbox = self.browser.find_element(By.ID, 'id_new_item')
		assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

		# They enter "Buy replacement drum heads" into a textbox
		inputbox.send_keys('Buy replacement drum heads')

		# When they hit enter, the page updates and "1. Buy replacement drum heads" is 
		# now listed as the first to-do list item
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy replacement drum heads')

		# There is still a text box inviting them to add another item. They enter 
		# "Replace old drum heads"
		inputbox = self.browser.find_element(By.ID, 'id_new_item')
		inputbox.send_keys('Replace old drum heads')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on the user's list, along
		# with another box to add more items
		self.wait_for_row_in_list_table('1: Buy replacement drum heads')
		self.wait_for_row_in_list_table('2: Replace old drum heads')

		# Satisfied, the user goes back to bed. 

	# using "request" fixture here instead of "browser"
	# so we can request a new browser session halfway through
	## TODO: use two fixtures instead of calling the same one twice - there should be some kind of way to "reuse"
	def test_multiple_users_can_start_lists_at_different_urls(self, request):
		# A user starts a new to-do list
		browser = request.getfixturevalue('get_browser')
		browser.get(self.home_url)
		inputbox = browser.find_element(By.ID, 'id_new_item')
		inputbox.send_keys('Buy replacement drum heads')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy replacement drum heads')

		# The user notices their list has a unique URL
		user1_list_url = browser.current_url
		url_pattern = '/lists/.+'
		assert re.search(url_pattern, user1_list_url), f"{user1_list_url} does not match {url_pattern}"

		# Now a new user visits the site. 

		## We use a new browser session to make sure no info from the first user 
		## (e.g. cookies) is coming through
		browser = request.getfixturevalue('get_browser')

		# The second user visits the homepage. There is no sign of the first user's list
		browser.get(self.home_url)
		page_text = browser.find_element(By.TAG_NAME, 'body').text
		assert 'Buy replacement drum heads' not in page_text
		assert 'Replace old' not in page_text

		# The second user starts a new list by entering an item.
		inputbox = browser.find_element(By.ID, 'id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# The second user gets their own unique URL
		user2_list_url = browser.current_url
		assert re.search(url_pattern, user2_list_url), f"{user2_list_url} does not match {url_pattern}"
		assert user1_list_url != user2_list_url

		# Again, there is no trace of the first user's list
		page_text = browser.find_element(By.TAG_NAME, 'body').text
		assert 'Buy replacement drum heads' not in page_text
		assert 'Buy milk' in page_text

		# Satisfied, both users go back to sleep. 

