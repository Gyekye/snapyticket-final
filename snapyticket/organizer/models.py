from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
User = settings.AUTH_USER_MODEL

PAYMENT_OPTIONS = (
    ('MM','mobile money'),
    ('BA','bank account'),
)

PAYMENT_STATUS  = (
    ('PEND','PENDING'),
    ('SUCCESS','SUCCESSFUL'),
    ('CANCEL','CANCELLED'),
)

class VerifiedOrganizersManager(models.Manager):
    #* returns all organizers with their verfied status as True
    def get_queryset(self):
        return super().get_queryset().filter(is_approved=True, is_verified = True)
    
class ApprovedOrganizersManager(models.Manager):
    #* returns all organizers with their approved status as True
    def get_queryset(self):
        return super(ApprovedOrganizersManager,self).get_queryset.filter(is_approved=True)

class Organizer(models.Model):
    
    #* core informations
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='organizers_logos', default='default_organizer_logo')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    
    #* social accounts
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    #* important ceredentials
    is_verified = models.BooleanField(default=False)
    secret_id = models.SlugField(blank=True)
    is_approved = models.BooleanField(default=False)
    
    #* connecting model to manager
    objects = models.Manager()
    approved = ApprovedOrganizersManager()
    verified = VerifiedOrganizersManager()
    
    #* methods for the organizer model
    
    def __str__(self):
        return f'{self.name} - {self.user.username} - {self.secret_id}'
    
    def get_absolute_url(self):
        return reverse('organizer:update', kwargs={'pk': self.id})
    
    #* returns the unique secret ID of the asscociated organizer
    @property
    def get_secret_id(self):
        return self.secret_id
    
    #* returns the user profile associated with the organizer model
    @property
    def get_user_profile(self):
        return self.user.username
    
    #* returns the is verfied status of the organizer
    @property
    def is_verified_status(self):
        return self.is_verified
    
    #* returns the approved status of the organizer
    @property
    def is_approved_status(self):
        return self.is_approved
    
        
    
# ? function to generate the secret key of organizers when  the save method is called
def organizer_secret_key(sender, instance, *args, **kwargs):
    
    # ? creates the secret_id when the organizer is verified
    if instance.is_approved_status == True:
        instance.secret_id = slugify(instance.user) + '-' + slugify(instance.name)
        
        
    # ? if user has a secret Id , email it to them
    if instance.secret_id:
        # todo 
         # ! send email via an HTML Template
        send_mail(
        'Your Secret ID',
        f'This is your unique Secret ID:{instance.secret_id}',
        settings.EMAIL_HOST_USER,
        [instance.email],
        fail_silently=False,
        )
        
    if instance.is_verified_status == True:
        send_mail(
        'You Have Been verified',
        f'You have been verified organizer {instance.name}',
        settings.EMAIL_HOST_USER,
        [instance.email],
        fail_silently=False,
        )
    
# ? connect method with signal function
pre_save.connect(organizer_secret_key, sender=Organizer)


#* payment model 
class RequestPayment(models.Model):
    # Security Details
    organizer       = models.ForeignKey(Organizer,on_delete=models.CASCADE)
    secret_id       = models.CharField(max_length=200)
    ticket_code     = models.CharField(max_length=200)
    
    # receipient account details
    payment_option  = models.CharField(max_length=100,choices=PAYMENT_OPTIONS)
    name_on_account = models.CharField(max_length=100)
    account_number  = models.PositiveIntegerField()
    
    # amount to be paid
    amount          = models.PositiveIntegerField()
    
    # date requested and paid
    requested_on    = models.DateTimeField(auto_now_add=True)
    paid_on         = models.DateTimeField(default=timezone.now)
    
    # payment request status
    status          = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    
    #* Model methods
    def __str__(self):
        return self.organizer.name
    
    #* Model Properties
    @property
    def payment_status(self):
        return self.status
    
    #* Model meta 
    class Meta:
        verbose_name = _("Organizer's Payment Request")
        verbose_name_plural = _("Organizers payment requests")
        ordering = ['-requested_on']
        
    


