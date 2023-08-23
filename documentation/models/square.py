from django.db import models
from ckeditor.fields import RichTextField

class SquaresDocumentation(models.Model):
    documentation = RichTextField(verbose_name="Documentación")
    
    class Meta:
        db_table = 'squares_documentation'
        verbose_name = "Documentación"
        verbose_name_plural = "Documentación"
        default_permissions = []
        permissions = (
            ('add_squaresdocumentation', 'Adicionar documentación de Square'),
            ('change_squaresdocumentation', 'Editar documentación de Square'),
            ('view_squaresdocumentation', 'Ver documentación de Square'),
            ('delete_squaresdocumentation', 'Eliminar documentación de Square')
        )
    
    def __str__(self):
        return f"Documentación de Square"