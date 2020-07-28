from django.contrib import admin
from care.sms.models import Facility
from care.sms.models import QualtricsSubmission
from care.sms.models import Binding


class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_identity', 'liaisons', 'tag_list']
    search_fields = ['name', 'identity']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def get_identity(self, obj):
        return obj.identity

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    get_identity.short_description = 'UUID'


class BindingAdmin(admin.ModelAdmin):
    list_display = ['facility', 'address', 'opt_out']
    search_fields = ['address', 'opt_out']
    exclude = ['binding_sid', 'service_sid', 'binding_type']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['address', 'facility']
        else:
            return []


class QualtricsSubmissionAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'facility', 'new_cases']


admin.site.register(Binding, BindingAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(QualtricsSubmission, QualtricsSubmissionAdmin)
