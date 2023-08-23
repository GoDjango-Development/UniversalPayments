from django.db import models
from oauth2_provider.models import Application

class SquaresApplication(Application):
    application_id=models.CharField(verbose_name="ID de la Aplicacion", max_length=255, null=True)
    location_id=models.CharField(verbose_name="ID de Localización",max_length=100,null=True)
    access_token=models.CharField(verbose_name="Token de Acceso", max_length=255)
    environment=models.CharField(verbose_name="Entorno", max_length=50, choices=(('sandbox', 'sandbox'),
    ('production', 'production'),))
    
    class Meta:
        db_table = 'squares_application'
        verbose_name = "Aplicación"
        verbose_name_plural = "Aplicaciones"
        default_permissions = []
        permissions = (
            ('add_squaresapplication', 'Adicionar aplicaciones de Square'),
            ('change_squaresapplication', 'Editar aplicaciones de Square'),
            ('view_squaresapplication', 'Ver aplicaciones de Square'),
            ('delete_squaresapplication', 'Eliminar aplicaciones de Square')
        )
        
    def __str__(self):
        return self.name