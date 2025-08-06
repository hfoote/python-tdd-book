import pytest
from pytest_django.asserts import assertRedirects
import accounts.views
from accounts.models import Token
from django.contrib import auth

@pytest.mark.django_db
class SendLoginEmailViewTest():

	def test_redirects_to_home_page(self, client):
		response = client.post('/accounts/send_login_email', data={
			'email':'big_foote@example.com'
		})
		assertRedirects(response, '/')

	def test_sends_mail_to_address_from_post(self, client, mocker):

		mock_send_mail = mocker.patch('accounts.views.send_mail')
		client.post('/accounts/send_login_email', data={
			'email': 'big_foote@example.com'
		})

		assert mock_send_mail.called == True
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args # zeroth element is args, first is kwargs
		assert subject == 'Your login link for Superlists'
		assert from_email == 'big_foote@myyahoo.com'
		assert to_list == ['big_foote@example.com']

	def test_adds_success_message(self, client):
		response = client.post('/accounts/send_login_email', data={
			'email':'big_foote@example.com'
		}, follow=True)

		message = list(response.context['messages'])[0]
		assert message.message == "Check your email, we've sent you a link you can use to log in."
		assert message.tags == 'success'

@pytest.mark.django_db
class LoginViewTest():

	def test_redirects_to_home_page(self, client, mocker):
		mock_auth = mocker.patch('accounts.views.auth')
		response = client.get('/accounts/login?abc123')
		assertRedirects(response, '/')

	def test_creates_token_associated_with_email(self, client):
		client.post('/accounts/send_login_email', data={
			'email':'big_foote@example.com'
		})
		token = Token.objects.first()
		assert token.email == 'big_foote@example.com'

	def test_sends_link_to_login_using_token_uid(self, client, mocker):
		mock_send_mail = mocker.patch('accounts.views.send_mail')
		client.post('/accounts/send_login_email', data={
			'email':'big_foote@example.com'
		})

		token = Token.objects.first()
		expected_url = f'http://testserver/accounts/login?token={token.uid}'

		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		assert expected_url in body

	def test_calls_authenticate_with_uid_from_get_request(self, client, mocker):
		mock_auth = mocker.patch('accounts.views.auth')
		client.get('/accounts/login?token=abc123')
		assert mock_auth.authenticate.call_args == mocker.call('abc123')

	def test_calls_auth_login_with_user_if_there_is_one(self, client, mocker):
		mock_auth = mocker.patch('accounts.views.auth')
		response = client.get('/accounts/login?token=abc123')
		assert mock_auth.login.call_args == mocker.call(response.wsgi_request, mock_auth.authenticate.return_value)

	def test_does_not_login_if_user_is_not_authenticated(self, client, mocker):
		mock_auth = mocker.patch('accounts.views.auth')
		mock_auth.authenticate.return_value = None
		client.get('/accounts/login?token=abc123')
		assert mock_auth.login.called == False