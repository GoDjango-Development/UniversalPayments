from django.db import models
from oauth2_provider.models import Application

class StripeApplication(Application):
    api_public_key = models.CharField(max_length=250, verbose_name="PUBLIC KEY", null=True, blank=True)
    api_secret_key = models.CharField(max_length=250, verbose_name="SECRET KEY", null=True, blank=True)
    
    class Meta:
        db_table = 'stripe_application'
        verbose_name = "Aplicación"
        verbose_name_plural = "Aplicaciones"
        default_permissions = []
        permissions = (
            ('add_stripeapplication', 'Adicionar aplicaciones de Stripe'),
            ('change_stripeapplication', 'Editar aplicaciones de Stripe'),
            ('view_stripeapplication', 'Ver aplicaciones de Stripe'),
            ('delete_stripeapplication', 'Eliminar aplicaciones de Stripe')
        )
        
    def __str__(self):
        return self.name