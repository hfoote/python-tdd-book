# my version of the test suite with pytest

from selenium import webdriver
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
	pytest.fail('Finish the test!')

	# The user is invited to enter a to-do list item

	# They enter "Buy replacement drum heads" into a textbox

	# When they hit enter, the page updates and "1. Buy replacement drum heads" is 
	# now listed as the first to-do list item

	# There is still a text box inviting them to add another item. They enter 
	# "replace old drumheads"

	# The page updates again, and now shows both items on the user's list, along
	# with another box to add more items

	# The user wonders whether the site will remember their list. They see some
	# text explaining that the site has genetrated a unique url for them which will 
	# store their list. 

	# The user opens their unique URL and sees their list

	# Satisfied, the user goes back to bed. 
