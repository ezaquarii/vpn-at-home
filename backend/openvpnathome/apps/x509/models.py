from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_x509.base.models import AbstractCa, AbstractCert

User = get_user_model()


class Ca(AbstractCa):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta(AbstractCa.Meta):
        abstract = False


class Cert(AbstractCert):

    TYPE_CLIENT = 'client'
    TYPE_SERVER = 'server'
    TYPES = (
        (TYPE_CLIENT, 'Client'),
        (TYPE_SERVER, 'Server')
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ca = models.ForeignKey(Ca, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=TYPES)
    common_name = models.CharField(_('common name'), max_length=63, blank=True, unique=True)

    class Meta(AbstractCert.Meta):
        abstract = False
