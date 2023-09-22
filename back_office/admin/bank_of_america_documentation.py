from django.contrib import admin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from documentation.forms import BankOfAmericaDocumentationForm
from documentation.models import BankOfAmericaDocumentation


class BankOfAmericaDocumentationAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 20
    form = BankOfAmericaDocumentationForm
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['model_name'] = 'bankofamericadocumentation'
        return super().add_view(request, form_url, extra_context=extra_context)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['model_name'] = 'bankofamericadocumentation'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        first_obj = self.model.objects.first()
        if first_obj is not None:
            if request.user.is_superuser:
                return redirect(reverse('admin:documentation_bankofamericadocumentation_change', args=(first_obj.pk,)))
            else:
                return redirect(reverse_lazy('object_details', kwargs={'model_name': 'bankofamericadocumentation', 'pk': first_obj.pk}))
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        if not BankOfAmericaDocumentation.objects.all():
            return True
        else:
            return False
        
    def has_delete_permission(self, request, obj=None):
        return False
        
BankOfAmericaDocumentationAdmin.save_as_continue = False
BankOfAmericaDocumentationAdmin.save_as = False
    
admin.site.register(BankOfAmericaDocumentation, BankOfAmericaDocumentationAdmin)