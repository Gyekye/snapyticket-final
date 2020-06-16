from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist


# Overrriding UserCreation and UserChange Forms

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
        ]

    def clean_phone(self):
        data = self.cleaned_data['phone']
        try:
            existing_phone=User.objects.get(phone=data)
            if existing_phone:
                raise forms.ValidationError('A user with this phone number already exists')
        except ObjectDoesNotExist:
            pass
        if len(data) < 10 or len(data) > 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits')
        return data

            
        
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'profile_image'
        ]

    def clean_phone(self):
        data = self.cleaned_data['phone']
        try:
            existing_phone = User.objects.get(phone=data)
            if existing_phone:
                raise forms.ValidationError('A user with this phone number already exists')
        except ObjectDoesNotExist:
            pass
        if len(data) < 10 or len(data) > 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits')
        return data