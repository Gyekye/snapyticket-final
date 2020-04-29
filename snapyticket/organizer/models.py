from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Organizer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='organizers_logos', default='default_organizer_logo')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    is_verified = models.BooleanField(default=False)
    # Todo Add the organizer social media links to the organizer model
    def get_absolute_url(self):
        return reverse('organizer:update', kwargs={'pk':self.id})
    


class Social(models.Model):
    organizer = models.ForeignKey(Organizer,on_delete=models.CASCADE)
    platform = models.CharField(max_length=50,blank=True)
    link = models.URLField(blank=True)
    
    def __str__(self):
        return f'{self.organizer.name} - {self.platform}'
    
    def get_social_url(self):
        return reverse('organizer:update_social', kwargs={'pk':self.id})
    # Todo Delets this model