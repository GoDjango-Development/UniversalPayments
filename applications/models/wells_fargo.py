from django.db import models
from oauth2_provider.models import Application

class WellsFargoApplication(Application):
    api_id = models.CharField(max_length=100, verbose_name="CONSUMER KEY", null=True, blank=True)
    api_secret = models.CharField(max_length=100, verbose_name="CONSUMER SECRET", null=True, blank=True)
    
    class Meta:
        db_table = 'wellsfargo_application'
        verbose_name = "Aplicación"
        verbose_name_plural = "Aplicaciones"
        default_permissions = []
        permissions = (
            ('add_wellsfargoapplication', 'Adicionar aplicaciones de Wells Fargo'),
            ('change_wellsfargoapplication', 'Editar aplicaciones de Wells Fargo'),
            ('view_wellsfargoapplication', 'Ver aplicaciones de Wells Fargo'),
            ('delete_wellsfargoapplication', 'Eliminar aplicaciones de Wells Fargo')
        )
        
    def __str__(self):
        return self.name