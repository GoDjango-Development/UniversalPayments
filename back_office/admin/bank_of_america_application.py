from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.urls import resolve

from applications.forms import BankOfAmericaApplicationForm
from applications.models import BankOfAmericaApplication


class BankOfAmericaApplicationAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 20
    form = BankOfAmericaApplicationForm
    list_display = ('title_column', 'get_client_id', 'get_user', 'get_created', 'action_column')
    search_fields = ('name',)
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            # Return all objects for superusers
            return BankOfAmericaApplication.objects.all()
        else:
            # Return only objects created by the current user
            return BankOfAmericaApplication.objects.filter(user=request.user)
    
    def get_client_id(self, obj):
        return obj.client_id

    get_client_id.allow_tags = False
    get_client_id.short_description = "ID de cliente"
    
    def get_user(self, obj):
        return obj.user
    
    get_user.short_description = "Usuario"

    def get_created(self, obj):
        return obj.created
    
    get_created.short_description = "Fecha de creación"
        
    def title_column(self, obj):
        return mark_safe('<a href="%s" style="cursor: pointer;" data-toggle="tooltip" title="%s"><b>%s</b></a>' % (
            reverse_lazy('object_details', kwargs={'model_name': 'bankofamericaapplication', 'pk': obj.pk}),
            "Detalles",
            obj.name
        ))

    title_column.allow_tags = True
    title_column.short_description = 'Nombre'
    title_column.admin_order_field = 'name'
    
    def action_column(self, obj):
        html = '<a href="%s" style="cursor: pointer; margin-right: 10px;" data-toggle="tooltip" title="%s">' \
               '   <i class="fas fa-edit text-primary" style="font-size: 14px;"></i>' \
               '</a>' % (
                   '/admin/applications/bankofamericaapplication/%i' % (obj.pk,),
                   "Editar"
               )
        html += '<a href="%s" style="cursor: pointer;" data-toggle="tooltip" class="btn-delete" title="%s">' \
                '   <i class="fas fa-trash text-danger" style="font-size: 14px;"></i>' \
                '</a>' % (
                    '/admin/applications/bankofamericaapplication/%i/delete/' % (obj.pk,),
                    "Eliminar"
                )
        return mark_safe(html)
    
    action_column.allow_tags = True
    action_column.short_description = "Acciones"
    
    def save_model(self, request, obj, form, change):
        obj.client_type = 'confidential'
        obj.authorization_grant_type = 'password'
        obj.user = request.user
        result = super().save_model(request, obj, form, change)
        return result
    
admin.site.register(BankOfAmericaApplication, BankOfAmericaApplicationAdmin)