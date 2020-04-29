from django import forms 
from .models import Organizer


class UpdateOrganizerInfo(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = [
            'name',
            'logo',
            'email',
        ]