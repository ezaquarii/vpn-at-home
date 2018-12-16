# admin.py of your app
from django.contrib import admin

from django_x509.base.admin import CaAdmin as BaseCaAdmin
from django_x509.base.admin import CertAdmin as BaseCertAdmin

from .models import Ca, Cert


class CaAdmin(BaseCaAdmin):
    fields = ['operation_type',
              'name',
              'owner',
              'notes',
              'key_length',
              'digest',
              'validity_start',
              'validity_end',
              'country_code',
              'state',
              'city',
              'organization_name',
              'email',
              'common_name',
              'extensions',
              'serial_number',
              'certificate',
              'private_key',
              'created',
              'modified']


class CertAdmin(BaseCertAdmin):

    list_display = ['name',
                    'type',
                    'key_length',
                    'digest',
                    'created',
                    'modified']

    fields = ['operation_type',
              'name',
              'owner',
              'ca',
              'type',
              'notes',
              'revoked',
              'revoked_at',
              'key_length',
              'digest',
              'validity_start',
              'validity_end',
              'country_code',
              'state',
              'city',
              'organization_name',
              'email',
              'common_name',
              'extensions',
              'serial_number',
              'certificate',
              'private_key',
              'created',
              'modified']


admin.site.register(Ca, CaAdmin)
admin.site.register(Cert, CertAdmin)