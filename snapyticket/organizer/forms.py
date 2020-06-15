from django import forms
from .models import Organizer

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
        ]
        

