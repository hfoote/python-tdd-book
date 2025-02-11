# my version of the test suite with pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pytest
import re
import os

MAX_WAIT = 10 # max time to wait for a row to populate in s

# setup / teardown function for the browser
@pytest.fixture
def browser(live_server):
	driver = webdriver.Firefox()
	yield driver
	driver.quit()

# fixture for the server url - returns either the specified staging sever
# or a pytest-django live_server url
@pytest.fixture
def home_url(live_server):
	staging_server = os.environ.get('STAGING_SERVER')
	if staging_server:
		yield 'http://' + staging_server
	else:
		yield live_server.url

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
def test_can_start_a_list_for_one_user(browser, home_url):

	# A user has heard about a new to-do app. They open the homepage
	browser.get(home_url)

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

# using "request" fixture here instead of "browser"
# so we can request a new browser session halfway through
## TODO: use two fixtures instead of calling the same one twice - there should be some kind of way to "reuse"
def test_multiple_users_can_start_lists_at_different_urls(request, home_url):
	# A user starts a new to-do list
	browser = request.getfixturevalue('browser')
	browser.get(home_url)
	inputbox = browser.find_element(By.ID, 'id_new_item')
	inputbox.send_keys('Buy replacement drum heads')
	inputbox.send_keys(Keys.ENTER)
	wait_for_row_in_list_table(browser, '1: Buy replacement drum heads')

	# The user notices their list has a unique URL
	user1_list_url = browser.current_url
	url_pattern = '/lists/.+'
	assert re.search(url_pattern, user1_list_url), f"{user1_list_url} does not match {url_pattern}"

	# Now a new user visits the site. 

	## We use a new browser session to make sure no info from the first user 
	## (e.g. cookies) is coming through
	browser = request.getfixturevalue('browser')

	# The second user visits the homepage. There is no sign of the first user's list
	browser.get(home_url)
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
	assert re.search(url_pattern, user2_list_url), f"{user2_list_url} does not match {url_pattern}"
	assert user1_list_url != user2_list_url

	# Again, there is no trace of the first user's list
	page_text = browser.find_element(By.TAG_NAME, 'body').text
	assert 'Buy replacement drum heads' not in page_text
	assert 'Buy milk' in page_text

	# Satisfied, both users go back to sleep. 

def test_layout_and_styling(browser, home_url):
	# A user goes to the home page
	browser.get(home_url)
	browser.set_window_size(1024, 768)

	# they notice the input box is nicely centered
	inputbox = browser.find_element(By.ID, 'id_new_item')
	# for some reason this gets put at x=44, but this test will still fail if CSS isn't loading, 
	# as it changes the width of the input box. 
	assert abs(inputbox.location['x'] + inputbox.size['width']/2 - (44+228)) <= 10 

	# they start a new list and notice the input box 
	# is centered in the list view page too
	inputbox.send_keys('testing')
	inputbox.send_keys(Keys.ENTER)
	wait_for_row_in_list_table(browser, '1: testing')
	inputbox = browser.find_element(By.ID, 'id_new_item')
	assert abs(inputbox.location['x'] + inputbox.size['width']/2 - (44+228)) <= 10 # same difference from book