from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

from rest_framework import status

from vpnathome.tests import APITestWithBaseFixture

User = get_user_model()


class RegisterUser(APITestWithBaseFixture):

    TEST_EMAIL = 'xray@test.com'
    TEST_PASSWORD = 'xray123'

    url = reverse('accounts-api:register')
    register_dto = {'email': TEST_EMAIL, 'password': TEST_PASSWORD}

    def setUp(self):
        self.assertEqual(0, User.objects.filter(email=self.TEST_EMAIL).count(), 'Test user already in database')
        response = self.client.post(self.url, self.register_dto)
        self.assertResponseOk(response)

    def test_user_is_registered(self):
        User.objects.get(email=self.TEST_EMAIL)

    def test_user_password_is_set(self):
        user = authenticate(username=self.TEST_EMAIL, password=self.TEST_PASSWORD)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.TEST_EMAIL)

    def test_email_is_unique(self):
        response = self.client.post(self.url, {'email': self.TEST_EMAIL, 'password': 'other password'})
        self.assertStatus(response, status.HTTP_400_BAD_REQUEST)

    def test_user_is_active(self):
        user = User.objects.get(email=self.TEST_EMAIL)
        self.assertTrue(user.is_active)
