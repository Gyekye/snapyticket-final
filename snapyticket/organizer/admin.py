from django.contrib import admin
from .models import Organizer
# Register your models here.

class OrganizerAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'name',
        'email',
        'is_verified',
        'logo',
    ]
admin.site.register(Organizer,OrganizerAdmin)
#admin.site.register(Social)
