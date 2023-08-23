from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse_lazy, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from oauth2_provider.models import Application
from django.forms.models import modelform_factory
from django.contrib import admin

from misc.forms import ApplicationForm


class ApplicationAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 20
    form = ApplicationForm
    list_display = ('title_column', 'get_client_id', 'get_user', 'get_created', 'action_column')
    search_fields = ('name',)
    
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
            reverse_lazy('object_details', kwargs={'model_name': 'application', 'pk': obj.pk}),
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
                   '/admin/oauth2_provider/application/%i' % (obj.pk,),
                   "Editar"
               )
        html += '<a href="%s" style="cursor: pointer;" data-toggle="tooltip" class="btn-delete" title="%s">' \
                '   <i class="fas fa-trash text-danger" style="font-size: 14px;"></i>' \
                '</a>' % (
                    '/admin/oauth2_provider/application/%i/delete/' % (obj.pk,),
                    "Eliminar"
                )
        return mark_safe(html)
    
    action_column.allow_tags = True
    action_column.short_description = "Acciones"
    
    def save_model(self, request, obj, form, change):
        obj.client_type = 'confidential'
        obj.authorization_grant_type = 'password'
        result = super().save_model(request, obj, form, change)
        return result
    
class GenerateNewClientSecretView(View):
    application = None

    def get_application(self):
        self.application = get_object_or_404(Application, pk=self.kwargs.get('pk'))
        
    def render_to_response(self, context):
        return HttpResponse(render(self.request, 'admin/oauth2_provider/application/change_form.html', context))

    def get(self, request, *args, **kwargs):
        self.get_application()
        if self.application:
            from oauth2_provider.generators import generate_client_secret
            client_secret = generate_client_secret()
            self.application.client_secret = client_secret
            self.application.save()
            ApplicationForm = modelform_factory(Application, fields=('name', 'client_id', 'client_secret',))
            form = ApplicationForm(instance=self.application, initial={'client_secret': client_secret})
            context = {
                'form': form,
                'is_popup': False,
                'save_as': False,
                'has_delete_permission': True,
                'has_add_permission': True,
                'has_change_permission': True,
                'opts': Application._meta,
            }
            return self.render_to_response(context)
            # return redirect(reverse('admin:oauth2_provider_application_change', args=[self.application.pk]))
            # return HttpResponse(f"New secret for client ID {self.application.client_id}: {client_secret}")