import re
from django.core import mail 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import pytest

TEST_EMAIL = 'big_foote@example.com'
SUBJECT = "Your login link for Superlists"

class LoginTest(FunctionalTest):
	def test_login_using_magic_link(self):
		# A user goes to the awesome superlists site
		# and notices a login bar, they enter their email
		self.browser.get(self.home_url)
		self.browser.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(
			TEST_EMAIL, Keys.ENTER
		)

		# A message appears telling them the email has been sent
		def check_for_text_in_body(text):
			assert text in self.browser.find_element(By.TAG_NAME, 'body').text
		self.wait_for(check_for_text_in_body, "Check your email")

		# They check their email and find a message
		email = mail.outbox.pop()
		assert TEST_EMAIL in email.to
		assert SUBJECT == email.subject

		# It has a url link in it
		assert "Use this link to log in" in email.body
		url_search = re.search(r"http://.+/.+$", email.body)
		if not url_search:
			pytest.fail(f"Could not find url in email body:\n{email.body}")
		url = url_search.group(0)
		assert self.home_url in url

		# The user clicks it
		self.browser.get(url)

		# they are logged in
		def check_logged_in():
			return self.browser.find_element(By.CSS_SELECTOR, "#id_logout")
		self.wait_for(check_logged_in)

		navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
		assert TEST_EMAIL in navbar.text

		# now they log out
		self.browser.find_element(By.CSS_SELECTOR, "#id_logout").click()

		# they are logged out
		def check_logged_out():
			return self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
		self.wait_for(check_logged_out)

		navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
		assert TEST_EMAIL not in navbar.text

