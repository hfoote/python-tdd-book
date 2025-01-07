import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains, assertRedirects
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

## Home page tests
@pytest.mark.django_db
def test_uses_home_template(client): # NOTE: client fixture automatically gets the current client
	response = client.get('/')
	assertTemplateUsed(response, 'home.html')

## New list tests
@pytest.mark.django_db
def test_can_save_a_POST_request(client):
	response = client.post('/lists/new', data={'item_text': 'A new list item'})

	assert Item.objects.count() == 1
	new_item = Item.objects.first()
	assert new_item.text == 'A new list item'

@pytest.mark.django_db
def test_redirects_after_POST(client):
	response = client.post('/lists/new', data={'item_text': 'A new list item'})
	assertRedirects(response, '/lists/the-only-list-in-the-world/')

## List view page tests
@pytest.mark.django_db
def test_uses_list_template(client):
	response = client.get('/lists/the-only-list-in-the-world/')
	assertTemplateUsed(response, 'list.html')

@pytest.mark.django_db
def test_displays_all_items(client):
	list_ = List.objects.create()
	Item.objects.create(text='itemey 1', list=list_)
	Item.objects.create(text='itemey 2', list=list_)

	response = client.get('/lists/the-only-list-in-the-world/')

	assertContains(response, 'itemey 1')
	assertContains(response, 'itemey 2')	

## Database tests
@pytest.mark.django_db
def test_saving_and_retrieving_items():
	list_ = List()
	list_.save()

	first_item = Item()
	first_item.text = 'The first (ever) list item'
	first_item.list = list_
	first_item.save()

	second_item = Item()
	second_item.text = 'Item the second'
	second_item.list = list_
	second_item.save()

	saved_list = List.objects.first()
	assert saved_list == list_

	saved_items = Item.objects.all()
	assert saved_items.count() == 2

	first_saved_item = saved_items[0]
	second_saved_item = saved_items[1]
	assert first_saved_item.text == 'The first (ever) list item'
	assert first_saved_item.list == list_
	assert second_saved_item.text == 'Item the second'
	assert second_saved_item.list == list_