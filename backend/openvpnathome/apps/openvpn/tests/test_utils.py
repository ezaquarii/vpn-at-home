from unittest import TestCase
from ..utils import generate_tls_auth_key, generate_dhparams


class GenerateTlsAuthKey(TestCase):

    def setUp(self):
        self.key = generate_tls_auth_key()

    def test_key_has_no_comment_lines(self):
        self.assertFalse("#" in self.key)

    def test_key_output_has_multiple_lines(self):
        self.assertTrue(len(self.key.split()) > 1)


class GenerateDhParams(TestCase):

    def setUp(self):
        self.dhparams = generate_dhparams(bits=256)

    def test_dhparams_output_has_multiple_lines(self):
        self.assertTrue(len(self.dhparams.split()) > 1)
