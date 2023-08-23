from django.contrib import admin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from documentation.forms import WellsFargoDocumentationForm
from documentation.models import WellsFargoDocumentation


class WellsFargoDocumentationAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 20
    form = WellsFargoDocumentationForm
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        first_obj = self.model.objects.first()
        if first_obj is not None:
            if request.user.is_superuser:
                return redirect(reverse('admin:applications_wellsfargodocumentation_change', args=(first_obj.pk,)))
            else:
                return redirect(reverse_lazy('object_details', kwargs={'model_name': 'wellsfargodocumentation', 'pk': first_obj.pk}))
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        if not WellsFargoDocumentation.objects.all():
            return True
        else:
            return False
        
    def has_delete_permission(self, request, obj=None):
        return False
        
WellsFargoDocumentationAdmin.save_as_continue = False
WellsFargoDocumentationAdmin.save_as = False
    
admin.site.register(WellsFargoDocumentation, WellsFargoDocumentationAdmin)