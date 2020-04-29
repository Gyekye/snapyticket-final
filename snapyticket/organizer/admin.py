from django.contrib import admin
from .models import Organizer,Social
# Register your models here.


class SocialProfileInline(admin.TabularInline):
    min_num = 1
    model   = Social
    fields  = ['platform','link']


class OrganizerAdmin(admin.ModelAdmin):
    inlines = [SocialProfileInline]
    list_display = [
        'user',
        'name',
        'email',
        'is_verified',
        'logo',
    ]
admin.site.register(Organizer,OrganizerAdmin)
#admin.site.register(Social)
