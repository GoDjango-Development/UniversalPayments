from django import forms
from documentation.models import BankOfAmericaDocumentation
from ckeditor.widgets import CKEditorWidget


class BankOfAmericaDocumentationForm(forms.ModelForm):
    class Meta:
        model = BankOfAmericaDocumentation
        
        fields = '__all__'

        widgets = {
            'documentation': CKEditorWidget(attrs={'disable': True})
        }