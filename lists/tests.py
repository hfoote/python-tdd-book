import pytest
from pytest_django.asserts import assertTemplateUsed
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page 

@pytest.mark.django_db
def test_uses_home_template(client):
	response = client.get('/')
	assertTemplateUsed(response, 'home.html')

@pytest.mark.django_db
def test_can_save_a_POST_request(client):
	response = client.post('/', data={'item_text': 'A new list item'})
	assert 'A new list item' in response.content.decode()
	assertTemplateUsed(response, 'home.html')