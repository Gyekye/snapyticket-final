from django import forms
from .models import OrganizerRegister

class OrganizerRegisterForm(forms.ModelForm):
    class Meta:
        model = OrganizerRegister
        fields = [
            'logo',
            'name',
            'email',
            'instagram',
            'facebook',
            'telegram',
            'twitter',
        ]
        