import pytest
from pytest_django.asserts import assertTemplateUsed
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item 

@pytest.mark.django_db
def test_uses_home_template(client):
	response = client.get('/')
	assertTemplateUsed(response, 'home.html')

@pytest.mark.django_db
def test_can_save_a_POST_request(client):
	response = client.post('/', data={'item_text': 'A new list item'})

	assert Item.objects.count() == 1
	new_item = Item.objects.first()
	assert new_item.text == 'A new list item'

@pytest.mark.django_db
def test_redirects_after_POST(client):
	response = client.post('/', data={'item_text': 'A new list item'})
	assert response.status_code == 302
	assert response['location'] == '/'

@pytest.mark.django_db
def test_only_saves_items_when_necessary(client):
	client.get('/')
	assert Item.objects.count() == 0

@pytest.mark.django_db
def test_displays_all_list_items(client):
	Item.objects.create(text='itemey 1')
	Item.objects.create(text='itemey 2')

	response = client.get('/')

	assert 'itemey 1' in response.content.decode()
	assert 'itemey 2' in response.content.decode()

@pytest.mark.django_db
def test_saving_and_retrieving_items():
	first_item = Item()
	first_item.text = 'The first (ever) list item'
	first_item.save()

	second_item = Item()
	second_item.text = 'Item the second'
	second_item.save()

	saved_items = Item.objects.all()
	assert saved_items.count() == 2

	first_saved_item = saved_items[0]
	second_saved_item = saved_items[1]
	assert first_saved_item.text == 'The first (ever) list item'
	assert second_saved_item.text == 'Item the second'