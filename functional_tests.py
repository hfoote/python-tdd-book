# my version of the test suite with pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pytest

# setup / teardown function for the browser
@pytest.fixture
def browser():
	driver = webdriver.Firefox()
	yield driver
	driver.quit()

def test_can_start_a_list_and_retrieve_it_later(browser):

	# A user has heard about a new to-do app. They open the homepage
	browser.get("http://localhost:8000")

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
	time.sleep(1)

	table = browser.find_element(By.ID, 'id_list_table')
	rows = table.find_elements(By.TAG_NAME, 'tr')
	assert any(row.text == '1. Buy replacement drum heads' for row in rows), "New to-do item does not appear in table"

	# There is still a text box inviting them to add another item. They enter 
	# "replace old drumheads"
	pytest.fail('Finish the test!')

	# The page updates again, and now shows both items on the user's list, along
	# with another box to add more items

	# The user wonders whether the site will remember their list. They see some
	# text explaining that the site has genetrated a unique url for them which will 
	# store their list. 

	# The user opens their unique URL and sees their list

	# Satisfied, the user goes back to bed. 
