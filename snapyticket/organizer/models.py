from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Organizer(models.Model):
    # Todo write a functuality to send the organizer ID to organizers when they regsiter as organizers
    # todo #3 write necesaary querysets for event organizers
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='organizers_logos', default='default_organizer_logo')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    secret_id = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse('organizer:update', kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.name} - {self.user.username} - {self.secret_id}'
