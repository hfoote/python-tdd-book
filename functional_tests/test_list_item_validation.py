# my version of the test suite with pytest

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import pytest

@pytest.mark.django_db
class ItenValidationTest(FunctionalTest):
	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit 
		# an empty list item. She hits enter on the empty input box. 

		# The home page refreshes, and there is an error message saying
		# that the list cannot be blank. 

		# She tries again with some text for this item, which now works. 

		# For some reason, she decides to submit a second empty list item. 

		# She recieves a similar warning on the list page. 

		# And she can correct it by filling some text in. 
		pytest.fail('write me!')