from django.contrib import admin
from .models import Ticket,TicketImage
# Register your models here.
class TicketImageInline(admin.TabularInline):
    min_num = 1
    model = TicketImage
    fields = ['image']


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    inlines = [TicketImageInline]
    list_display = [
        'title',
        'slug',
        'category',
        'organizer',
    ]
admin.site.register(Ticket,TicketAdmin)