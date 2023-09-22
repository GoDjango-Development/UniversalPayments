from django.db import models
from oauth2_provider.models import Application


ENVIRONMENTS = (
    ('apitest.cybersource.com', 'test'),
    ('api.cybersource.com', 'production'),
)


class BankOfAmericaApplication(Application):
    merchant_id = models.CharField(max_length=100, verbose_name="Merchant ID", null=True, blank=True)
    key = models.CharField(max_length=100, verbose_name="Key", null=True, blank=True)
    shared_secret_key = models.CharField(max_length=100, verbose_name="Shared secret key", null=True, blank=True)
    run_environment = models.CharField(verbose_name="Entorno", max_length=50, choices=ENVIRONMENTS)
    
    class Meta:
        db_table = 'bankofamerica_application'
        verbose_name = "Aplicación"
        verbose_name_plural = "Aplicaciones"
        default_permissions = []
        permissions = (
            ('add_bankofamericaapplication', 'Adicionar aplicaciones de Bank of America'),
            ('change_bankofamericaapplication', 'Editar aplicaciones de Bank of America'),
            ('view_bankofamericaapplication', 'Ver aplicaciones de Bank of America'),
            ('delete_bankofamericaapplication', 'Eliminar aplicaciones de Bank of America')
        )
        
    def __str__(self):
        return self.name