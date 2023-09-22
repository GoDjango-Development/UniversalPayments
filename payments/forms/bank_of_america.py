from django import forms
from payments.models import BankOfAmericaPayment


class BankOfAmericaPaymentForm(forms.ModelForm):
    
    class Meta:
        model = BankOfAmericaPayment

        exclude = ('user',)