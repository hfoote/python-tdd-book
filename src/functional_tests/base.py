# my version of the test suite with pytest

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pytest

MAX_WAIT = 10 # max time to wait for a row to populate in sec

# wait decorator
def wait(fn):
		def modified_fn(*args, **kwargs):
			start_time = time.time()
			while True:
				try:
					return fn(*args, **kwargs)
				except (AssertionError, WebDriverException) as e:
					if time.time() - start_time > MAX_WAIT:
						raise e
					time.sleep(0.5)
		return modified_fn

class FunctionalTest: # base functional test class that will be inherited by others
	# always fetch the browser and home url fixtures, and place them into attributes
	@pytest.fixture(autouse=True) # TODO: try to get rid of this now that you have conftest set up
	def _setup(self, get_browser, get_home_url):
		self.browser = get_browser
		self.home_url = get_home_url

	@wait
	def wait_for_row_in_list_table(self, row_text):
		table = self.browser.find_element(By.ID, 'id_list_table')
		rows = table.find_elements(By.TAG_NAME, 'tr')
		assert row_text in [row.text for row in rows]

	@wait
	def wait_for(self, fn, *args):
		return fn(*args)

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element(By.CSS_SELECTOR, "#id_logout")
		navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
		assert email in navbar.text

	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
		navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
		assert email not in navbar.text

	def get_item_input_box(self):
		return self.browser.find_element(By.ID, 'id_text')
