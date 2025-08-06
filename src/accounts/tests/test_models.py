from django.contrib.auth import get_user_model
from accounts.models import Token
import pytest
from django.contrib import auth

User = get_user_model()

@pytest.mark.django_db
class UserModelTest():

	def test_user_is_valid_with_email_only(self):
		user = User(email='a@b.com')
		user.full_clean()

	def test_email_is_primary_key(self):
		user = User(email='a@b.com')
		assert user.pk == 'a@b.com'

	def test_no_problem_with_auth_login(self, client):
		user = User.objects.create(email='big_foote@example.com')
		user.backend = ''
		request = client.request().wsgi_request
		auth.login(request, user)

@pytest.mark.django_db
class TokenModelTest():
	def test_links_user_with_auto_generated_uid(self):
		token1 = Token.objects.create(email='a@b.com')
		token2 = Token.objects.create(email='a@b.com')
		assert token1.uid != token2.uid
