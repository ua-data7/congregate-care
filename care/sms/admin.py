from django.contrib import admin
from care.sms.models import Facility


class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'liasons', 'tags']


admin.site.register(Facility, FacilityAdmin)
