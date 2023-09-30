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

class StripePayment(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, null=True, blank=True)
    stripe_app = models.ForeignKey(Application, verbose_name="Aplicación", on_delete=models.CASCADE, null=True, blank=True)    
    amount=models.FloatField(verbose_name="Cantidad de dinero a pagar",null=True)
    transaction_uuid = models.CharField(verbose_name="UUID de transacción", max_length=100)
    currency=models.CharField(verbose_name="Tipo de Moneda",max_length=20,null=True)    
    status = models.CharField(max_length=15, verbose_name="Estado", default='pending', choices=STATUSES)
    datetime = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    
    class Meta:
        db_table = 'stripe_payment'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        default_permissions = []
        ordering = ('-datetime',)
        permissions = (
            ('add_stripepayment', 'Adicionar pagos de Stripe'),
            ('change_stripepayment', 'Editar pagos de Stripe'),
            ('view_stripepayment', 'Ver pagos de Stripe'),
            ('delete_stripepayment', 'Eliminar pagos de Stripe')
        )
        
    def get_status_as_html(self):
        return mark_safe(
            f'<span class="badge text-white" style="background: {STATUS_COLOR[self.status]}">'
            f'  {self.get_status_display().upper()}'
            f'</span>'
        )
        
    def __str__(self):
        return self.transaction_uuid