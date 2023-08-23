from django import forms
from documentation.models import WellsFargoDocumentation
from ckeditor.widgets import CKEditorWidget


class WellsFargoDocumentationForm(forms.ModelForm):
    class Meta:
        model = WellsFargoDocumentation
        
        fields = '__all__'

        widgets = {
            'documentation': CKEditorWidget(attrs={'disable': True})
        }