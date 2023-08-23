from django.db import models
from ckeditor.fields import RichTextField
    
class WellsFargoDocumentation(models.Model):
    documentation = RichTextField(verbose_name="Documentación")
    
    class Meta:
        db_table = 'wellsfargo_documentation'
        verbose_name = "Documentación"
        verbose_name_plural = "Documentación"
        default_permissions = []
        permissions = (
            ('add_wellsfargodocumentation', 'Adicionar documentación de Wells Fargo'),
            ('change_wellsfargodocumentation', 'Editar documentación de Wells Fargo'),
            ('view_wellsfargodocumentation', 'Ver documentación de Wells Fargo'),
            ('delete_wellsfargodocumentation', 'Eliminar documentación de Wells Fargo')
        )
    
    def __str__(self):
        return f"Documentación de Wells Fargo"