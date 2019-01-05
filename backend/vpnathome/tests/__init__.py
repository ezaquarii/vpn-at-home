"""
This module provides all test fixtures and test-related utilities.
"""

from unittest import skipIf

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from vpnathome.tests import fixture
from .fixture import FixtureBuilder, BaseFixtureMixin

User = get_user_model()


def is_email_configured():
    from django.conf import settings
    return all([settings.EMAIL_HOST,
                settings.EMAIL_PORT,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_HOST_PASSWORD,
                settings.EMAIL_ENABLED,
                settings.SERVER_EMAIL])


def configRequired(precondition, reason):
    """
    Test annotation. Test will be skipped if specific config precondition is false.
    It's just a normal skipIf annotation with some more descriptive message.

    :param precondition: Check config.
    :param reason: Skip reason.
    :return: skipIf instance
    """
    message = "{reason}\nPlease run './manage.py configure' and inspect configuration.".format(reason=reason)
    return skipIf(not precondition, message)


def skip_if_email_not_configured():
    return skipIf(not is_email_configured(), 'This test requires e-mail configuration. '
                                             'Inspect your settings.json and re-run the test')


class TestWithBaseFixture(TestCase, BaseFixtureMixin):

    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()
        cls.load_base_fixture()


class APITestWithBaseFixture(APITestCase, BaseFixtureMixin):

    @classmethod
    def setUpClass(cls):
        super(APITestCase, cls).setUpClass()
        cls.load_base_fixture()

    def assertResponseOk(self, response):
        self.assertTrue(response.status_code >= 200 and response.status_code <= 300,
                        msg='HTTP code not 2xx. Actual code: {code}, errors: {errors}'.format(code=response.status_code,
                                                                                              errors=response.data))

    def assertUnauthorized(self, response, message=None):
        from rest_framework import status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertForbidden(self, response, message=None):
        from rest_framework import status
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertNotFound(self, response, message=None):
        from rest_framework import status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertStatus(self, response, status, message=None):
        self.assertEqual(response.status_code, status, message)


def is_running_under_test():
    import sys
    return 'test' in sys.argv
