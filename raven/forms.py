from django import forms
from .models import RavenFiles

class RavenForm(forms.ModelForm):
    class Meta:
        model = RavenFiles
        fields=("r_file",)