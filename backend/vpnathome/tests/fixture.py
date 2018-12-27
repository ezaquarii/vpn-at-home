"""
This module contains test fixtures used for all tests in all other applications.
"""

from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from vpnathome.apps.management.models import BlockedDomain
from vpnathome.apps.openvpn.models import DhParams
from vpnathome.apps.openvpn.serializers import CreateServerSerializer, CreateClientSerializer
from vpnathome.utils import get_object_or_none


# Generating DH params is quite time consuming. This test fixture is used to speed
# up tests, but should never be used to initialize production data
TEST_DHPARAM_2048 = '-----BEGIN DH PARAMETERS-----'\
                    'MIIBCAKCAQEA92+jaEDJjqq2CpaxHE1N2v87toSh5HqWVS+2goCfnvgtPpKASjHp'\
                    '243hZVaQAKJ0FHzK9WY7kMYSTeAezN7dXRRqdM7FB7PqSEFQMps0/NcCHLu/0gbB'\
                    'APiicY2ZXVhBYfXNwjtCxlmb7Sm/2WRoar9odgLEJinHsGCtnm4R0sHncYA/XEps'\
                    'B4pltJbjtqAQkk/N4XGP5kE3uflEK5qU3VMgKXiL3apj2alQlY2EDAnmfE9+mMlY'\
                    'XANWtj9cugGf0aEba35GBxL8dfiZQyiJld9BUM7aJMN+qNDG8mxY+RurE16zeZnP'\
                    'NDKek/9Ea53qobLHPuPohSBtPDALO42gIwIBAg=='\
                    '-----END DH PARAMETERS-----'


User = get_user_model()


class FixtureBuilder(object):
    """
    This helper class is used to build initial test fixture.
    """

    class Fixture():
        def __init__(self):
            self.admin = None
            self.server = None
            self.users = []
            self.clients = []
            self.dhparams = None
            self.dns_blocked_domains = []

    def __init__(self):
        self._fixture = FixtureBuilder.Fixture()

    def get_shared_fixture(self):
        return self._fixture

    def dhparams(self):
        self._fixture.dhparams = DhParams.objects.create(dhparams=TEST_DHPARAM_2048)

    def admin(self, email):
        admin = User.objects.create(email=email, is_staff=True, is_superuser=True)
        admin.set_password(email)
        admin.save()
        self._fixture.admin = admin
        return self

    def user(self, email):
        user = User.objects.create(email=email)
        user.set_password(user)
        user.save()
        self._fixture.users.append(user)
        return self

    def users(self, emails):
        for email in emails:
            self.user(email)

    def auth_tokens(self):
        for user in User.objects.all():
            Token.objects.create(user=user)

    def server(self, name='Server', hostname='hostname', deploy_dns=False):
        assert self._fixture.admin, 'Admin user is required'
        assert self._fixture.dhparams, 'DH params are required'
        context = dict(owner=self._fixture.admin, dhparams=self._fixture.dhparams)
        server_dto = dict(
            name=name,
            hostname=hostname,
            email=self._fixture.admin.email,
            deploy_dns=deploy_dns
        )
        create_serializer = CreateServerSerializer(data=server_dto, context=context)
        create_serializer.is_valid(raise_exception=True)
        self._fixture.server = create_serializer.save()
        return self

    def client(self, name, owner_email):
        assert self._fixture.admin, 'Admin user is required'
        user = get_object_or_none(User, email=owner_email)
        assert user, 'Owner user {} doesnt exist'.format(owner_email)
        assert user in self._fixture.users or user == self._fixture.admin, 'User must be created by Given'
        assert self._fixture.server, 'Server is required'
        context = dict(owner=user, server=self._fixture.server)
        client_dto = dict(name=name)
        create_serializer = CreateClientSerializer(data=client_dto, context=context)
        create_serializer.is_valid(raise_exception=True)
        client = create_serializer.save()
        self._fixture.clients.append(client)
        return self

    def dns_blocked_domain(self, domain):
        domain_object = BlockedDomain.objects.create(domain=domain)
        self._fixture.dns_blocked_domains.append(domain_object)


class BaseFixtureMixin(object):
    """
    Base fixture used for API tests. It provides bare minimum data
    to play various scenarios. It also provides some helper
    properties to quickly perform authenticated API calls.

    * 4 users (1 admin, 3 normals)
    * authenticated APIClients to send REST calls
    * unauthenticated APIClient
    * token and user properties
    * test dhparams
    """

    # You can override user names in derived test cases to use different e-mail
    # addresses. This can be useful if you want to test e-mail functionality with
    # real e-mail account.
    TEST_USER_ADMIN = 'admin@vpnathome.net'
    TEST_USER_ALPHA = 'alpha@vpnathome.net'
    TEST_USER_BRAVO = 'bravo@vpnathome.net'
    TEST_USER_CHARLIE = 'charlie@vpnathome.net'

    @classmethod
    def load_base_fixture(cls):
        DhParams.objects.create(dhparams=TEST_DHPARAM_2048)
        cls.builder = FixtureBuilder()
        cls.builder.admin(cls.TEST_USER_ADMIN)
        cls.builder.users([cls.TEST_USER_ALPHA, cls.TEST_USER_BRAVO, cls.TEST_USER_CHARLIE])
        cls.builder.auth_tokens()
        cls.builder.dhparams()

        # this object is shared with builder and can be enriched by subclasses by
        # further calls to builder instance
        cls.fixture = cls.builder.get_shared_fixture()

    @property
    def dhparams(self):
        return self.fixture.dhparams

    @property
    def test_user_admin(self):
        return User.objects.get(email=self.TEST_USER_ADMIN)

    @property
    def test_user_admin_token(self):
        return Token.objects.get(user__email=self.TEST_USER_ADMIN)

    @property
    def test_user_alpha(self):
        return User.objects.get(email=self.TEST_USER_ALPHA)

    @property
    def test_user_alpha_token(self):
        return Token.objects.get(user__email=self.TEST_USER_ALPHA)

    @property
    def test_user_bravo(self):
        return User.objects.get(email=self.TEST_USER_BRAVO)

    @property
    def test_user_bravo_token(self):
        return Token.objects.get(user__email=self.TEST_USER_BRAVO)

    @property
    def test_user_charlie(self):
        return User.objects.get(email=self.TEST_USER_CHARLIE)

    @property
    def test_user_charlie_token(self):
        return Token.objects.get(user__email=self.TEST_USER_CHARLIE)

    @property
    def admin_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_admin_token.key)
        return client

    @property
    def alpha_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_alpha_token.key)
        return client

    @property
    def bravo_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_bravo_token.key)
        return client

    @property
    def charlie_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_charlie_token.key)
        return client