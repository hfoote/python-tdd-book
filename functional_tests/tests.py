# my version of the test suite with pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pytest
import re

MAX_WAIT = 10 # max time to wait for a row to populate in s

# setup / teardown function for the browser
@pytest.fixture
def browser():
	driver = webdriver.Firefox()
	yield driver
	driver.quit()

def wait_for_row_in_list_table(browser, row_text):
	start_time = time.time()
	while True:
		try:
			table = browser.find_element(By.ID, 'id_list_table')
			rows = table.find_elements(By.TAG_NAME, 'tr')
			assert row_text in [row.text for row in rows]
			return
		except (AssertionError, WebDriverException) as e:
			if time.time() - start_time > MAX_WAIT:
				raise e
			time.sleep(0.5)

# NOTE : live_server fixture runs a separate test server, then cleans up (equivalent of django.test.LiveServerTestCase)
def test_can_start_a_list_and_retrieve_it_later(browser, live_server):

	# A user has heard about a new to-do app. They open the homepage
	browser.get(live_server.url)

	# and see that the page mentions to-do lists in its title
	assert "To-Do" in browser.title
	header_text = browser.find_element(By.TAG_NAME, 'h1').text
	assert "To-Do" in header_text

	# The user is invited to enter a to-do list item
	inputbox = browser.find_element(By.ID, 'id_new_item')
	assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

	# They enter "Buy replacement drum heads" into a textbox
	inputbox.send_keys('Buy replacement drum heads')

	# When they hit enter, the page updates and "1. Buy replacement drum heads" is 
	# now listed as the first to-do list item
	inputbox.send_keys(Keys.ENTER)
	wait_for_row_in_list_table(browser, '1: Buy replacement drum heads')

	# There is still a text box inviting them to add another item. They enter 
	# "Replace old drum heads"
	inputbox = browser.find_element(By.ID, 'id_new_item')
	inputbox.send_keys('Replace old drum heads')
	inputbox.send_keys(Keys.ENTER)

	# The page updates again, and now shows both items on the user's list, along
	# with another box to add more items
	wait_for_row_in_list_table(browser, '1: Buy replacement drum heads')
	wait_for_row_in_list_table(browser, '2: Replace old drum heads')

	# Satisfied, the user goes back to bed. 

def test_multiple_users_can_start_lists_at_different_urls(browser, live_server):
	# A user starts a new to-do list
	browser.get(live_server.url)
	inputbox = browser.find_element(By.ID, 'id_new_item')
	inputbox.send_keys('Buy replacement drum heads')
	inputbox.send_keys(Keys.ENTER)
	wait_for_row_in_list_table(browser, '1: Buy replacement drum heads')

	# The user notices their list has a unique URL
	user1_list_url = browser.current_url
	assert re.search('/lists/.+', user1_list_url), f"{user1_list_url} does not match '/lists/.+'"

	# Now a new user visits the site. 

	## We use a new browser session to make sure no info from the first user 
	## (e.g. cookies) is coming through
	browser.quit()
	browser = webdriver.Firefox()

	# The second user visits the homepage. There is no sign of the first user's list
	browser.get(live_server.url)
	page_text = browser.find_element(By.TAG_NAME, 'body').text
	assert 'Buy replacement drum heads' not in page_text
	assert 'Replace old' not in page_text

	# The second user starts a new list by entering an item.
	inputbox = browser.find_element(By.ID, 'id_new_item')
	inputbox.send_keys('Buy milk')
	inputbox.send_keys(Keys.ENTER)
	wait_for_row_in_list_table(browser, '1: Buy milk')

	# The second user gets their own unique URL
	user2_list_url = browser.current_url
	assert re.search('/lists/.+', user2_list_url), f"{user2_list_url} does not match '/lists/.+'"
	assert user1_list_url != user2_list_url

	# Again, there is no trace of the first user's list
	page_text = browser.find_element(By.TAG_NAME, 'body').text
	assert 'Buy replacement drum heads' not in page_text
	assert 'Buy milk' in page_text

	# Satisfied, both users go back to sleep. 
