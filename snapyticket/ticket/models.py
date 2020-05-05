from django.db import models
from organizer.models import Organizer
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
# Create your models here.
CATEGORY_CHOICES = (
    ('CS', "Concert Show"),
    ('SS', "Summit Show"),
    ('MS', "Movie Show"),
    ('FS', "Sports Event"),
    ('PS', "Party Event"),
    ('ES', "Other Event"),
)

class Ticket(models.Model):
    # todo Write querysets to send emails to organizers who have their tickets pending 
    # todo write querysets to generate all buyers of specific organizers ticket
    """ 
    An event organizer can have multiple tickets
    A Ticket should be based in a particular category of events
    A Ticket should have a pricing 
    A Ticket should have a discount in the form of coupons 
    A Ticket should have a unique ID
    A Ticket should have multiple photos of the event
    A Ticket should have a setting which includes dates and venue
    A Ticket can be in most featured or featured or can be just normal 
    """ 
    # organizer
    organizer = models.ForeignKey(Organizer,on_delete=models.CASCADE)
    
    #  main details
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(help_text = 'This will be auto-generated [Unique Ticket ID]',default='Slug-Field')
    featured_image = models.ImageField(upload_to='ticket_images')
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=10)
    
    # Pricing 
    start_price = models.PositiveIntegerField()
    end_price = models.PositiveIntegerField()
    
    # Date and Time
    date_deadline = models.DateTimeField()
    start_date_time = models.DateTimeField()
    end_date_and_time = models.DateTimeField()

    # Venue
    venue = models.CharField(max_length=100)
    city  = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    
    # Features
    is_suggested = models.BooleanField(default=False)
    is_featured  = models.BooleanField(default=False)
    is_most_featured = models.BooleanField(default=False)
    
    # Model Methods 
    def __str__(self):
        return f'{self.title} created by {self.organizer.user.username}'
    
    def get_absolute_url(self):
        return reverse("ticket:detail", kwargs={"slug": self.slug})
    
    
# model signals 
# todo write a custom signal to send ticket ID to organizers
def ticket_slug_slugify(sender,instance,*args, **kwargs):
    """ Auto Generates Ticket Slug and then sends the unique ID to the event organizer"""
    instance.slug = slugify(instance.title)+'-'+slugify(instance.organizer.name)
    send_mail(
    'Your Ticket ID',
    f'This is your unique Ticket ID:{instance.slug}',
    settings.EMAIL_HOST_USER,
    [instance.organizer.email],
    fail_silently=False,
    )
pre_save.connect(ticket_slug_slugify,sender=Ticket)


class TicketImage(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='ticket_images')


class TicketVariation(models.Model):
    ticket =  models.ForeignKey(Ticket,on_delete=models.CASCADE)
    variation = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.ticket.title} - {self.variation}'