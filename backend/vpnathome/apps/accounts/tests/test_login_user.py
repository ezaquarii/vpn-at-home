from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

from rest_framework import status

from vpnathome.tests import APITestWithBaseFixture

User = get_user_model()


class LoginUser(APITestWithBaseFixture):

    url = reverse('accounts-api:login')

    def test_user_is_logged_in(self):
        login_dto = {
            'email': self.TEST_USER_ALPHA,
            'password': self.TEST_USER_ALPHA
        }
        self.response = self.client.post(self.url, login_dto)
        self.assertResponseOk(self.response)
        self.assertTrue('sessionid' in self.response.cookies)

    def test_user_is_not_logged_in_with_invalid_password(self):
        login_dto = {
            'email': self.TEST_USER_ALPHA,
            'password': 'invalid password'
        }
        self.response = self.client.post(self.url, login_dto)
        self.assertStatus(self.response, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('sessionid' in self.response.cookies)
