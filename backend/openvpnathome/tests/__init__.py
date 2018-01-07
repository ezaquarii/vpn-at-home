"""
This module provides all test fixtures and test-related utilities.
"""

from unittest import skipIf

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from openvpnathome import CONFIG_PATH
from openvpnathome.tests import fixture
from .fixture import FixtureBuilder, BaseFixtureMixin

User = get_user_model()


def configRequired(precondition, reason):
    """
    Test annotation. Test will be skipped if specific config precondition is false.
    It's just a normal skipIf annotation with some more descriptive message.

    :param precondition: Check config.
    :param reason: Skip reason.
    :return: skipIf instance
    """
    message = "{reason}\nPlease run './manage.py configure' and inspect configuration in '{config_path}'.".format(reason=reason,
                                                                                                                  config_path=CONFIG_PATH)
    return skipIf(not precondition, message)


class APITestWithBaseFixture(APITestCase, BaseFixtureMixin):

    @classmethod
    def setUpClass(cls):
        super(APITestCase, cls).setUpClass()
        cls.load_base_fixture()

    def assertResponseOk(self, response):
        self.assertTrue(response.status_code >= 200 and response.status_code <= 300,
                        msg='HTTP code not 2xx. Actual code: {code}, errors: {errors}'.format(code=response.status_code,
                                                                                              errors=response.data))

    def assertUnauthorized(self, response):
        from rest_framework import status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertForbidden(self, response):
        from rest_framework import status
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertStatus(self, response, status, message=None):
        self.assertEqual(response.status_code, status, message)


