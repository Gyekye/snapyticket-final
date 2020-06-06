from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


User = settings.AUTH_USER_MODEL

# Create your models here.

class VerifiedOrganizersManager(models.Manager):
    # returns all organizers with their verfied status as True
    def get_queryset(self):
        return super().get_queryset().filter(is_verfied = True)

class OrganizerRegister(models.Model):
    # Todo write a functuality to send the organizer ID to organizers when they regsiter as organizers
    # todo #3 write necesaary querysets for event organizers
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='organizers_logos_register', default='default_organizer_logo')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    secret_id = models.SlugField(blank=True)
    
    # connecting model to manager
    objects = models.Manager()
    verified = VerifiedOrganizersManager()
    
    # methods for the organizer model
    
    def __str__(self):
        return f'{self.name} - {self.user.username} - {self.secret_id}'
    
    def get_absolute_url(self):
        return reverse('organizer:update', kwargs={'pk': self.id})
    
    # returns the unique secret ID of the asscociated organizer
    @property
    def get_secret_id(self):
        return self.secret_id
    
    # returns the user profile associated with the organizer model
    @property
    def get_user_profile(self):
        return self.user.username
    
    # returns the is verfied status of the organizer
    @property
    def is_verified_status(self):
        return self.is_verified
    


