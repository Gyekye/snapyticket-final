from django.contrib import admin
from .models import Ticket,TicketImage,TicketVariation,TicketItem,TicketBag
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
class TicketBagAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'created_on',
        'order_ref_code',
        'ordered',
    ]
class TicketItemAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ticket',
        'ticket_type',
        'quantity',
    ]
admin.site.register(Ticket,TicketAdmin)
admin.site.register(TicketBag,TicketBagAdmin)
admin.site.register(TicketItem,TicketItemAdmin)