import pytest
from lists.models import Item, List
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class ItemModelTest:

	def test_default_text(self):
		item = Item()
		assert item.text == ''

	def test_item_is_related_to_list(self):
		list_ = List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		assert item in list_.item_set.all()

	def test_cannot_save_empty_list_items(self):
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with pytest.raises(ValidationError):
			item.save()
			item.full_clean()

	def test_duplicate_items_are_invalid(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='bla')
		with pytest.raises(ValidationError):
			item = Item(list=list_, text='bla')
			item.full_clean()

	def test_CAN_save_same_item_to_different_lists(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='bla')
		item = Item(list=list2, text='bla')
		item.full_clean() # should NOT raise

	def test_list_ordering(self):
		list_ = List.objects.create()
		item1 = Item.objects.create(list=list_, text='i1')
		item2 = Item.objects.create(list=list_, text='item 2')
		item3 = Item.objects.create(list=list_, text='3')
		assert list(Item.objects.all()) == [item1, item2, item3]

	def test_string_representation(self):
		item = Item(text='some text')
		assert str(item) == 'some text'

@pytest.mark.django_db
class ListModelTest:

	def test_get_absolute_url(self):
		list_ = List.objects.create()
		assert list_.get_absolute_url() == f'/lists/{list_.id}/'