# This file holds all of the fixtures needed by other tests

import pytest
from selenium import webdriver
import os

# setup / teardown function for the browser
@pytest.fixture
def get_browser():
	driver = webdriver.Firefox()
	yield driver
	driver.quit()

# fixture for the server url - returns either the specified staging sever
# or a pytest-django live_server url
@pytest.fixture
def get_home_url(live_server):
	test_server = os.environ.get('TEST_SERVER')
	if test_server:
		yield 'http://' + test_server
	else:
		yield live_server.url