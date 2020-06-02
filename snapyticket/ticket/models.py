from django.db import models
from organizer.models import Organizer
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

# Create your models here.
CATEGORY_CHOICES = (
    ('CT', "Concert Ticket"),
    ('ST', "Summit Ticket"),
    ('MT', "Movie Ticket"),
    ('ET', "Esports Ticket"),
    ('PT', "Party Ticket"),
    ('OT', "Other Ticket"),
)
# Managers for the various types of tickets 

# concert tickets
class ConcertTicketManager(models.Manager):
    def get_queryset(self):
        return super(ConcertTicketManager,self).get_queryset().filter(category='CT')
# summit tickets   
class SummitTicketManager(models.Manager):
    def get_queryset(self):
        return super(SummitTicketManager,self).get_queryset().filter(category='ST')
# movie tickets 
class MovieTicketManager(models.Manager):
    def get_queryset(self):
        return super(MovieTicketManager,self).get_queryset().filter(category='MT')
# esports tickets  
class EsportTicketManager(models.Manager):
    def get_queryset(self):
        return super(EsportTicketManager,self).get_queryset().filter(category='ET')
# party tickets 
class PartyTicketManager(models.Manager):
    def get_queryset(self):
        return super(PartyTicketManager,self).get_queryset().filter(category='PT')
# other tickets  
class OtherTicketManager(models.Manager):
    def get_queryset(self):
        return super(OtherTicketManager,self).get_queryset().filter(category='OT')
    
class Ticket(models.Model):
    # todo Write queryset to send emails to organizers who have their tickets pending
    # todo write queryset to generate all buyers of specific organizers ticket
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
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    #  main details
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(help_text='This will be auto-generated [Unique Ticket ID]', default='Slug-Field', max_length=1000)
    featured_image = models.ImageField(upload_to='ticket_images')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)

    # Pricing 
    start_price = models.PositiveIntegerField()
    end_price = models.PositiveIntegerField()

    # Date and Time
    date_deadline = models.DateTimeField()
    start_date_time = models.DateTimeField()
    end_date_and_time = models.DateTimeField()

    # Venue
    venue = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    map_location = models.CharField(max_length=1200, blank=True, null=True)

    # Features
    is_suggested = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_most_featured = models.BooleanField(default=False)
    
    # hooking models to managers
    objects = models.Manager()
    parties  = PartyTicketManager()
    summits  = SummitTicketManager()
    concerts = ConcertTicketManager() 
    movies   = MovieTicketManager()
    esports  = EsportTicketManager()
    others   = OtherTicketManager()
    # Model Methods 
    def __str__(self):
        return f'{self.title} created by {self.organizer.name}'
    # absolute url
    def get_absolute_url(self):
        return reverse("ticket:detail", kwargs={"slug": self.slug})
    # add to cart url 
    def add_to_cart(self):
        return reverse("ticket:add_to_cart", kwargs={"slug": self.slug})


# model signals 
# todo write a custom signal to send ticket ID to organizers
# todo uncomment the sending email functionality
def ticket_slug_slugify(sender, instance, *args, **kwargs):
    """ Auto Generates Ticket Slug and then sends the unique ID to the event organizer"""
    instance.slug = slugify(instance.title) + '-' + slugify(instance.organizer.name)
    """
    send_mail(
    'Your Ticket ID',
    f'This is your unique Ticket ID:{instance.slug}',
    settings.EMAIL_HOST_USER,
    [instance.organizer.email],
    fail_silently=False,
    )
    """
pre_save.connect(ticket_slug_slugify, sender=Ticket)


class TicketImage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ticket_images')


class TicketVariation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    variation = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ticket.title} - {self.variation}'


# Main ticket Item Model
class TicketItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ticket_type = models.ForeignKey(TicketVariation, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    slug = models.SlugField(default="Slug-Field")
    ticket_code = models.CharField(max_length=15,blank=True)
    
    
    # named object representation
    def __str__(self):
        return f'{self.ticket.title}-{self.ticket_type}-{self.quantity}-{self.user.username}'
    
    # aboslute url

    
    # cart to remove from cart
    def remove_from_cart(self):
        return reverse('ticket:remove_from_cart', kwargs={'slug': self.slug, 'pk': self.pk})
    
    # update ticket_item url
    def update_ticket_item(self):
        return reverse('ticket:update_ticket_item', kwargs={'slug': self.slug, 'pk': self.pk})
    
    # setting the price of the ticket item
    def ticket_item_price(self):
        return self.quantity * self.ticket_type.price
    
    # total price method Note: Always call this method when wanting to get the ticket item price
    def ticket_item_total_price(self):
        return self.ticket_item_price()

#   A signal to generate a unique slug for each Ticket item
def ticket_item_slug_gen(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.user) + '-' + slugify(instance.ticket.title)
pre_save.connect(ticket_item_slug_gen, sender=TicketItem)

# model to hold qr _code of ticket item model
class TicketItemQrImage(models.Model):
    ticket_item = models.ForeignKey(TicketItem,on_delete=models.CASCADE)
    ticket_item_qr_image = models.ImageField(upload_to='ticket_qr_code')
  
  
  
  
# Manager to get all ordered ticket bag     
class OrderedTicketBag(models.Manager):
    def get_queryset(self):
        return super(OrderedTicketBag,self).get_queryset().filter(ordered=True)   
    
# actual ticket bag model   
class TicketBag(models.Model):
    # todo write custom queryset to get all ordered and unordered querysets
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(TicketItem)
    created_on = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    order_ref_code = models.CharField(max_length=100,blank=True)
    
    # hooking manager to model 
    objects = models.Manager()
    ordered_ticket_bags = OrderedTicketBag()
    
    # model methods 
    def __str__(self):
        return f'{self.user.username} - ticket-bag'
    
    # absolute url
    def get_absolute_url(self):
        return reverse('profile:bag-detail', kwargs={'order_ref_code': self.order_ref_code})
    
    # getting the total price of Ticket bag 
    def total_ticket_bag_price(self):
        total_price = 0
        # loops through the ticket items 
        for ticket_items in self.tickets.all():
            # appends the ticket item price to the total_price variable
            total_price += ticket_items.ticket_item_total_price()
        return total_price

class SavedTickets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, blank=True, null=True)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.ticket.title} - {self.user}'
