import pytest
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page 

@pytest.mark.django_db
def test_root_url_resolves_to_home_page_view():
	found = resolve('/')
	assert found.func == home_page

@pytest.mark.django_db
def test_home_page_returns_correct_html():
	request = HttpRequest()
	response = home_page(request)
	html = response.content.decode('utf8')
	
	assert html.startswith('<html>')
	assert '<title>To-Do Lists</title>' in html
	assert html.endswith('</html>')