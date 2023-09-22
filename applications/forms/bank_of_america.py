from django import forms
from applications.models import BankOfAmericaApplication


class BankOfAmericaApplicationForm(forms.ModelForm):
    custom_header = forms.CharField(label='DATOS DE CYBERSOURCE.COM', disabled=True, required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}))
    
    class Meta:
        model = BankOfAmericaApplication

        fields = ['client_id', 'client_secret', 'name', 'custom_header', 'merchant_id', 'key', 'shared_secret_key', 'run_environment']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'data-show-length': True}),
            'client_id': forms.TextInput(attrs={'class': 'form-control', 'data-show-length': True}),
            'client_secret': forms.TextInput(attrs={'class': 'form-control', 'data-show-length': True})
        }

        labels = {
            'name': 'nombre',
            'client_secret': 'secreto de cliente',
            'client_id': 'ID de cliente'
        }
