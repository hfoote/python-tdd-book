import pytest
from django.urls import resolve
from lists.views import home_page 

@pytest.mark.django_db
def test_root_url_resolves_to_home_page_view():
	found = resolve('/')
	assert found.func == home_page