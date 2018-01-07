from django.contrib import admin
from .models import DhParams, Client, Server


class ServerAdmin(admin.ModelAdmin):
    pass


admin.site.register(DhParams, ServerAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Client, ServerAdmin)
