# my version of the test suite with pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pytest

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

	# The user wonders whether the site will remember their list. They see some
	# text explaining that the site has genetrated a unique url for them which will 
	# store their list. 
	pytest.fail('Finish the test!')

	# The user opens their unique URL and sees their list

	# Satisfied, the user goes back to bed. 
