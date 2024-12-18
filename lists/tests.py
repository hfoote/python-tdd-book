import pytest
from pytest_django.asserts import assertTemplateUsed
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page 

@pytest.mark.django_db
def test_home_page_returns_correct_html(client):
	response = client.get('/')
	assertTemplateUsed(response, 'home.html')