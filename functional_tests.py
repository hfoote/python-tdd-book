# test suite as written in the book with unittest

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):

		# A user has heard about a new to-do app. They open the homepage
		self.browser.get("http://localhost:8000")

		# and see that the page mentions to-do lists in tis title
		# changed from book assertion as my version of Django has a different 
		# title
		self.assertIn("To-Do", self.browser.title)
		self.fail('Finish the test!')

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


if __name__ == "__main__":
	unittest.main(warnings='ignore')