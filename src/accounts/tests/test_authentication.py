import pytest
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from django.contrib import auth
from accounts.models import Token

User = get_user_model()

@pytest.mark.django_db
class AuthenticateTest():
	
	def test_returns_None_if_no_such_token(self):
		result = PasswordlessAuthenticationBackend().authenticate(
			'no-such-token'
		)
		assert result == None
	
	def test_returns_new_user_with_correct_email_if_token_exists(self):
		email = 'big_foote@example.com'
		token = Token.objects.create(email=email)
		user = PasswordlessAuthenticationBackend().authenticate(token.uid)
		new_user = User.objects.get(email=email)
		assert user == new_user
	
	def test_returns_existing_user_with_correct_email_if_token_exists(self):
		email = 'big_foote@example.com'
		existing_user = User.objects.create(email=email)
		token = Token.objects.create(email=email)
		user = PasswordlessAuthenticationBackend().authenticate(token.uid)
		assert user == existing_user

	def test_returns_existing_user_with_correct_email_if_token_exists_with_custom_backend(self):
		email = 'big_foote@example.com'
		existing_user = User.objects.create(email=email)
		token = Token.objects.create(email=email)
		user = auth.authenticate(token.uid)
		assert user == existing_user

@pytest.mark.django_db
class GetUserTest():

	def test_gets_user_by_email(self):
		User.objects.create(email='another@example.com')
		desired_user = User.objects.create(email='big_foote@example.com')
		found_user = PasswordlessAuthenticationBackend().get_user(
			'big_foote@example.com'
		)
		assert found_user == desired_user
	
	def test_returns_None_if_no_user_with_that_email(self):
		assert PasswordlessAuthenticationBackend().get_user('big_foote@example.com') == None