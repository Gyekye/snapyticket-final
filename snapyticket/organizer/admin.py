from django.contrib import admin
from .models import Organizer,RequestPayment
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ngettext
from django.contrib import messages
# Register your models here.

class OrganizerAdmin(admin.ModelAdmin):
    actions = ['approve_organizer']
    list_display = [
        'user',
        'name',
        'email',
        'is_verified',
        'is_approved',
        'secret_id',
    ]
    #* Custom admin actions on Organizer
    def approve_organizer(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, ngettext(
            '%d Organizer was successfully marked as verified.',
            '%d Organizers were successfully marked as verified.',
            updated,
        ) % updated, messages.SUCCESS)
    approve_organizer.short_description = "Approve Organizer as Verified"
    
admin.site.register(Organizer,OrganizerAdmin)
admin.site.register(RequestPayment)
