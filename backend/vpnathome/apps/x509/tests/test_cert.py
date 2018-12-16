from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from vpnathome.apps.x509.models import Cert, Ca

User = get_user_model()


class CertUniqueCommonNameTest(TestCase):
    """
    Common Name is used by OpenVPN to uniquely identify connected clients, hence the
    database must constraint it.
    """

    def setUp(self):
        self.user = User.objects.create(email='test@locahost')
        self.ca = Ca.objects.create(owner=self.user,
                               name='CA Name',
                               email=self.user.email,
                               common_name='CA Common Name')

        self.cert = Cert.objects.create(owner=self.user,
                                   ca=self.ca,
                                   name='Test Server Certificate Name',
                                   type=Cert.TYPE_SERVER,
                                   email=self.user.email,
                                   common_name='CA Common Name')

        self.assertEqual(1, Cert.objects.count())

    def __create_cert(self, common_name):
        """Helper to create client's cert; common name is the only difference"""
        Cert.objects.create(owner=self.user,
                            ca=self.ca,
                            name='Test Client Certificate Name',
                            type=Cert.TYPE_CLIENT,
                            email=self.user.email,
                            common_name=common_name)

    def test_cert_creation_with_unqiue_common_name_succeedes(self):
        self.__create_cert(self.cert.common_name + 'modified')
        self.assertEqual(2, Cert.objects.count())

    def test_cert_creation_with_duplicate_common_name_fails(self):
        with self.assertRaises(IntegrityError):
            self.__create_cert(self.cert.common_name)
