from django import forms
from applications.models import WellsFargoApplication


class WellsFargoApplicationForm(forms.ModelForm):
    class Meta:
        model = WellsFargoApplication

        fields = ['client_id', 'client_secret', 'name', 'api_id', 'api_secret']

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
