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

class SquaresPayment(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, null=True, blank=True)
    square_app = models.ForeignKey(Application, verbose_name="Aplicación", on_delete=models.CASCADE, null=True, blank=True)
    idempotency_key = models.CharField(verbose_name="ID de transacción", max_length=100,null=True)
    source_id=models.CharField(verbose_name="Fuente de Pago", max_length=100,null=True)
    amount=models.IntegerField(verbose_name="Cantidad de dinero a pagar",null=True)
    currency=models.CharField(verbose_name="Tipo de Moneda",max_length=20,null=True)
    customer_id=models.CharField(verbose_name="Cuenta de Destino", max_length=100,null=True)
    reference_id=models.CharField(verbose_name="ID Único de Tranferencia", max_length=100,null=True)
    status = models.CharField(max_length=15, verbose_name="Estado", default='pending', choices=STATUSES)
    datetime = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    
    class Meta:
        db_table = 'squares_payment'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        default_permissions = []
        ordering = ('-datetime',)
        permissions = (
            ('add_squarespayment', 'Adicionar pagos de Square'),
            ('change_squarespayment', 'Editar pagos de Square'),
            ('view_squarespayment', 'Ver pagos de Square'),
            ('delete_squarespayment', 'Eliminar pagos de Square')
        )
        
    def get_status_as_html(self):
        return mark_safe(
            f'<span class="badge text-white" style="background: {STATUS_COLOR[self.status]}">'
            f'  {self.get_status_display().upper()}'
            f'</span>'
        )
        
    def __str__(self):
        return self.idempotency_key