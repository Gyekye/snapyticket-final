from django.db import models
from django.contrib.auth.models import AbstractUser

from phone_field import PhoneField

# Creating a custom user model

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = PhoneField(help_text="Enter your phone number")
    is_organizer = models.BooleanField(help_text="Are you an event organizer",default=False)
    profile_image = models.ImageField(upload_to='profile/profile-images',blank=True)
    
    
    def __str__(self):
        return self.username