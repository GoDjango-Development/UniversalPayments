from django.db import models
from ckeditor.fields import RichTextField
    
class BankOfAmericaDocumentation(models.Model):
    documentation = RichTextField(verbose_name="Documentación")
    
    class Meta:
        db_table = 'bankofamerica_documentation'
        verbose_name = "Documentación"
        verbose_name_plural = "Documentación"
        default_permissions = []
        permissions = (
            ('add_bankofamericadocumentation', 'Adicionar documentación de Bank of America'),
            ('change_bankofamericadocumentation', 'Editar documentación de Bank of America'),
            ('view_bankofamericadocumentation', 'Ver documentación de Bank of America'),
            ('delete_bankofamericadocumentation', 'Eliminar documentación de Bank of America')
        )
    
    def __str__(self):
        return f"Documentación de Bank of America"