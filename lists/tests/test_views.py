import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains, assertRedirects, assertNotContains
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from django.utils.html import escape

@pytest.mark.django_db
class HomePageTest:

	def test_uses_home_template(self, client): # NOTE: client fixture automatically gets the current client
		response = client.get('/')
		assertTemplateUsed(response, 'home.html')

	def test_home_page_uses_item_form(self, client):
		response = client.get('/')
		assert isinstance(response.context['form'], ItemForm)

@pytest.mark.django_db
class NewListTest:

	def test_can_save_a_POST_request(self, client):
		response = client.post('/lists/new', data={'text': 'A new list item'})

		assert Item.objects.count() == 1
		new_item = Item.objects.first()
		assert new_item.text == 'A new list item'

	def test_redirects_after_POST(self, client):
		response = client.post('/lists/new', data={'text': 'A new list item'})
		new_list = List.objects.first()
		assertRedirects(response, f'/lists/{new_list.id}/')

	def test_for_invalid_input_renders_home_template(self, client):
		response = client.post('/lists/new', data={'text': ''})
		assert response.status_code == 200
		assertTemplateUsed(response, 'home.html')

	def test_validation_errors_are_shown_on_home_page(self, client):
		response = client.post('/lists/new', data={'text': ''})
		assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_for_invalid_input_passes_form_to_template(self, client):
		response = client.post('/lists/new', data={'text': ''})
		assert isinstance(response.context['form'], ItemForm)

	def test_invalid_list_items_arent_saved(self, client):
		client.post('/lists/new', data={'text': ''})
		assert List.objects.count() == 0
		assert Item.objects.count() == 0

@pytest.mark.django_db
class ListViewTest:

	def test_uses_list_template(self, client):
		list_ = List.objects.create()
		response = client.get(f'/lists/{list_.id}/')
		assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self, client):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)

		response = client.get(f'/lists/{correct_list.id}/')

		assertContains(response, 'itemey 1')
		assertContains(response, 'itemey 2')
		assertNotContains(response, 'other list item 1')
		assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self, client):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = client.get(f'/lists/{correct_list.id}/')
		assert response.context['list'] == correct_list

	def test_can_save_a_POST_request_to_an_existing_list(self, client):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		client.post(
			f'/lists/{correct_list.id}/',
			data = {'text': 'A new item for an existing list'}
		)

		assert Item.objects.count() == 1
		new_item = Item.objects.first()
		assert new_item.text == 'A new item for an existing list'
		assert new_item.list == correct_list

	def test_POST_redirects_to_list_view(self, client):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = client.post(
			f'/lists/{correct_list.id}/',
			data = {'text': 'A new item for an existing list'}
		)

		assertRedirects(response, f'/lists/{correct_list.id}/')

	def test_displays_item_form(self, client):
		list_ = List.objects.create()
		response = client.get(f'/lists/{list_.id}/')
		assert isinstance(response.context['form'], ItemForm)
		assertContains(response, 'name="text"')
		
	def post_invalid_input(self, client):
		list_ = List.objects.create()
		return client.post(
			f'/lists/{list_.id}/',
			data = {'text': ''}
		)
	
	def test_for_invalid_input_nothing_saved_to_db(self, client):
		self.post_invalid_input(client)
		assert Item.objects.count() == 0

	def test_for_invalid_input_renders_list_template(self, client):
		response = self.post_invalid_input(client)
		assert response.status_code == 200 
		assertTemplateUsed(response, 'list.html')	

	def test_for_invalid_input_passes_form_to_template(self, client):
		response = self.post_invalid_input(client)
		assert isinstance(response.context['form'], ItemForm)

	def test_for_invalid_input_shows_error_on_page(self, client):
		response = self.post_invalid_input(client)
		assertContains(response, escape(EMPTY_ITEM_ERROR))
