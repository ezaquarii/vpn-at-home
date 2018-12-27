from django.contrib import admin
from .models import Settings, BlockedDomain, BlockListUrl


class ManagementAdmin(admin.ModelAdmin):
    pass


admin.site.register(Settings, ManagementAdmin)
admin.site.register(BlockedDomain, ManagementAdmin)
admin.site.register(BlockListUrl, ManagementAdmin)
