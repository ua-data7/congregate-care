from django.contrib import admin
from care.sms.models import EnrolledUser, Facility


class EnrolledUserAdmin(admin.ModelAdmin):
    list_display = ['identity', 'name', 'created_date']
    search_fields = ['identity',]

class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'liasons', 'tags']

admin.site.register(EnrolledUser, EnrolledUserAdmin)
admin.site.register(Facility, FacilityAdmin)
