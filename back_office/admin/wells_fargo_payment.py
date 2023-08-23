from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from misc.utils.constants import SHORT_DATE_FORMAT, SHORT_TIME_FORMAT

from payments.forms import WellsFargoPaymentForm
from payments.models import WellsFargoPayment


class WellsFargoPaymentAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 20
    form = WellsFargoPaymentForm
    list_display = ('title_column', 'wells_fargo_app', 'get_datetime', 'get_status',)
    search_fields = ('wells_fargo_app',)
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            # Return all objects for superusers
            return WellsFargoPayment.objects.all()
        else:
            # Return only objects created by the current user
            return WellsFargoPayment.objects.filter(user=request.user)
    
    def get_status(self, obj):
        return obj.get_status_as_html()
    
    get_status.short_description = "Estado"
    
    def get_client_id(self, obj):
        return obj.client_id
    
    def get_datetime(self, obj):
        return mark_safe(
            '<i class="fa fa-calendar-alt"></i> <span class="margin-r-5">%s</span><i class="fa fa-clock ml-3"></i> %s' % (
                format(obj.datetime, SHORT_DATE_FORMAT), format(obj.datetime, SHORT_TIME_FORMAT))
        )
    
    get_datetime.short_description = "Fecha"
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        result = super().save_model(request, obj, form, change)
        return result
      
    def title_column(self, obj):
        return mark_safe('<a href="%s" style="cursor: pointer;" data-toggle="tooltip" title="%s"><b>%s</b></a>' % (
            reverse_lazy('object_details', kwargs={'model_name': 'wellsfargopayment', 'pk': obj.pk}),
            "Detalles",
            obj.transaction_uuid
        ))

    title_column.allow_tags = True
    title_column.short_description = 'UUID de transacción'
    title_column.admin_order_field = 'transaction_uuid'
    
    # def action_column(self, obj):
    #     html = '<a href="%s" style="cursor: pointer; margin-right: 10px;" data-toggle="tooltip" title="%s">' \
    #            '   <i class="fas fa-edit text-primary" style="font-size: 14px;"></i>' \
    #            '</a>' % (
    #                '/admin/wells_fargo/wellsfargopayment/%i' % (obj.pk,),
    #                "Editar"
    #            )
    #     html += '<a href="%s" style="cursor: pointer;" data-toggle="tooltip" class="btn-delete" title="%s">' \
    #             '   <i class="fas fa-trash text-danger" style="font-size: 14px;"></i>' \
    #             '</a>' % (
    #                 '/admin/wells_fargo/wellsfargopayment/%i/delete/' % (obj.pk,),
    #                 "Eliminar"
    #             )
    #     return mark_safe(html)
    
    # action_column.allow_tags = True
    # action_column.short_description = "Acciones"
    
    # def save_model(self, request, obj, form, change):
    #     obj.client_type = 'confidential'
    #     obj.authorization_grant_type = 'password'
    #     result = super().save_model(request, obj, form, change)
    #     return result
    
admin.site.register(WellsFargoPayment, WellsFargoPaymentAdmin)