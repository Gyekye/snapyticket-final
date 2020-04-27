from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import User
from django.core.exceptions import ValidationError


# Overrriding UserCreation and UserChange Forms

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
        ]      
            
        
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'profile_image'
        ]
    