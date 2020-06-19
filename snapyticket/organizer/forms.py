from django import forms
from .models import Organizer
from django.core.exceptions import ValidationError
# Form for registering as an  event organizer

class OrganizerRegisterForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = [
            'name',
            'email',
            'logo',
            'instagram',
            'facebook',
            'telegram',
            'twitter',
        ]
        


        

