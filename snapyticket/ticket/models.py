from django.db import models
from organizer.models import Organizer
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
    slug = models.SlugField(help_text = 'This will be auto-generated [Unique Ticket ID]')
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
    
    
    def __str__(self):
        return f'{self.title} created by {self.organizer.user.username}'

class TicketImage(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='ticket_images')
