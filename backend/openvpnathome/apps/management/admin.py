from django.contrib import admin
from .models import Settings


class ManagementAdmin(admin.ModelAdmin):
    pass


admin.site.register(Settings, ManagementAdmin)
