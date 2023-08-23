from django.db import models
from django.contrib.auth.models import User
from misc.models import Application
from django.utils.safestring import mark_safe


STATUSES = (
    ('pending', 'pendiente'),
    ('completed', 'completado'),
    ('rejected', 'rechazado'),
)

STATUS_COLOR = {
    'pending': '#958cd0',
    'completed': 'green',
    'rejected': '#ae3535',
}

class WellsFargoPayment(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, null=True, blank=True)
    wells_fargo_app = models.ForeignKey(Application, verbose_name="Aplicación", on_delete=models.CASCADE, null=True, blank=True)
    transaction_uuid = models.CharField(verbose_name="UUID de transacción", max_length=100)
    status = models.CharField(verbose_name="Estado", default='pending', choices=STATUSES, max_length=15)
    datetime = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    
    class Meta:
        db_table = "wellsfargo_payment"
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        default_permissions = []
        ordering = ('-datetime',)
        permissions = (
            ('add_wellsfargopayment', 'Adicionar pagos de Wells Fargo'),
            ('change_wellsfargopayment', 'Editar pagos de Wells Fargo'),
            ('view_wellsfargopayment', 'Ver pagos de Wells Fargo'),
            ('delete_wellsfargopayment', 'Eliminar pagos de Wells Fargo')
        )
        
    def get_status_as_html(self):
        return mark_safe(
            f'<span class="badge text-white" style="background: {STATUS_COLOR[self.status]}">'
            f'  {self.get_status_display().upper()}'
            f'</span>'
        )
        
    def __str__(self):
        return self.transaction_uuid
