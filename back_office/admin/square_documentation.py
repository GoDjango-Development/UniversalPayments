from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from documentation.forms import SquareDocumentationForm
from documentation.models import SquaresDocumentation


class SquareDocumentationAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 20
    form = SquareDocumentationForm
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        first_obj = self.model.objects.first()
        if first_obj is not None:
            if request.user.is_superuser:
                return redirect(reverse('admin:documentation_squaresdocumentation_change', args=(first_obj.pk,)))
            else:
                return redirect(reverse('admin:documentation_squaresdocumentation_change', args=(first_obj.pk,)))
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        if not SquaresDocumentation.objects.all():
            return True
        else:
            return False
        
    def has_delete_permission(self, request, obj=None):
        return False
        
SquareDocumentationAdmin.save_as_continue = False
SquareDocumentationAdmin.save_as = False
    
admin.site.register(SquaresDocumentation, SquareDocumentationAdmin)