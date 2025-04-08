# my version of the test suite with pytest

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pytest

MAX_WAIT = 10 # max time to wait for a row to populate in sec

class FunctionalTest: # base functional test class that will be inherited by others
	# always fetch the browser and home url fixtures, and place them into attributes
	@pytest.fixture(autouse=True)
	def _setup(self, get_browser, get_home_url):
		print("getting browser")
		self.browser = get_browser
		self.home_url = get_home_url

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element(By.ID, 'id_list_table')
				rows = table.find_elements(By.TAG_NAME, 'tr')
				assert row_text in [row.text for row in rows]
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)