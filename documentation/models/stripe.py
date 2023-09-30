from django.db import models
from ckeditor.fields import RichTextField

class StripeDocumentation(models.Model):
    documentation = RichTextField(verbose_name="Documentación")
    
    class Meta:
        db_table = 'stripe_documentation'
        verbose_name = "Documentación"
        verbose_name_plural = "Documentación"
        default_permissions = []
        permissions = (
            ('add_stripedocumentation', 'Adicionar documentación de Stripe'),
            ('change_stripedocumentation', 'Editar documentación de Stripe'),
            ('view_stripedocumentation', 'Ver documentación de Stripe'),
            ('delete_stripedocumentation', 'Eliminar documentación de Stripe')
        )
    
    def __str__(self):
        return f"Documentación de Stripe"