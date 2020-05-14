from django.contrib import admin

from care.sms.models import EnrolledUser, Facility, QualtricsSubmission, Binding



class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'liasons', 'tag_list']
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class BindingAdmin(admin.ModelAdmin):
    list_display = ['facility', 'address', 'opt_out']
    search_fields = ['address', 'opt_out']
    readonly_fields = ['address', 'facility']
    exclude = ['binding_sid', 'service_sid', 'binding_type']

class QualtricsSubmissionAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'facility', 'new_cases']

admin.site.register(Binding, BindingAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(QualtricsSubmission, QualtricsSubmissionAdmin)