from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Organizer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='organizers_logos', default='default_organizer_logo')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    is_verified = models.BooleanField(default=False)
    


class Social(models.Model):
    organizer = models.ForeignKey(Organizer,on_delete=models.CASCADE)
    platform = models.CharField(max_length=50,blank=True)
    link = models.URLField(blank=True)
    
    def __str__(self):
        return f'{self.organizer.name} - {self.platform}'
