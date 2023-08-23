from django import forms
from payments.models import WellsFargoPayment


class WellsFargoPaymentForm(forms.ModelForm):
    
    class Meta:
        model = WellsFargoPayment

        exclude = ('user',)