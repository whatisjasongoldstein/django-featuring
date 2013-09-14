from django.conf import settings
from django.contrib import admin
from .models import Dashboard, Thing
from genericadmin.admin import GenericAdminModelAdmin

class ThingInline(admin.TabularInline):
    model = Thing
    extra = 0
    fields = ['content_type', 'object_id', 'link_to_source', 'order']
    ordering = ['order',]
    readonly_fields = ['link_to_source',]

class DashboardAdmin(GenericAdminModelAdmin):
    model = Dashboard
    inlines = [ThingInline,]

    if hasattr(settings, 'FEATURABLE_CONTENT_TYPES'):
        content_type_whitelist = settings.FEATURABLE_CONTENT_TYPES
    

admin.site.register(Dashboard, DashboardAdmin)