from django import forms
from payments.models import StripePayment


class StripePaymentForm(forms.ModelForm):
    
    class Meta:
        model = StripePayment

        exclude = ('user',)