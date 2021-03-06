from django.conf import settings
from django.contrib import admin
from .models import Dashboard, Thing

class ThingInline(admin.TabularInline):
    model = Thing
    extra = 0
    fields = ['content_type','object_id','order',]
    ordering = ['order',]


class DashboardAdmin(admin.ModelAdmin):
    model = Dashboard
    inlines = [ThingInline,]

    if hasattr(settings, 'FEATURABLE_CONTENT_TYPES'):
        content_type_whitelist = settings.FEATURABLE_CONTENT_TYPES

admin.site.register(Dashboard, DashboardAdmin)
