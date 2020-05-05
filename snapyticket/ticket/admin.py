from django.contrib import admin
from .models import Ticket,TicketImage,TicketVariation
# Register your models here.
class TicketImageInline(admin.TabularInline):
    min_num = 1
    model = TicketImage
    fields = ['image']

class TicketVariation(admin.TabularInline):
    min_value  = 1
    model  = TicketVariation
    fields = ['variation','price']
    
# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    inlines = [TicketImageInline,TicketVariation]
    list_display = [
        'title',
        'slug',
        'category',
        'organizer',
    ]
admin.site.register(Ticket,TicketAdmin)