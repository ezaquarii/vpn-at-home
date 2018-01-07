import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(_('username'), unique=True, max_length=150, default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
