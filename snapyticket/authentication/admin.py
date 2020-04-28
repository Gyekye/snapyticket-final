from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from.forms import UserChangeForm,UserCreationForm
# Register your models here.

# Hooking Custom forms to Admin default forms
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    
    list_display = [
        'username',
        'email',
        'is_organizer',
        'phone',
        'is_staff',
        'is_active',
    ]
    fieldsets = (
        (None, {'fields': ('email', 'password','profile_image','phone',)}),
        ('Other Information', {'fields': ('is_organizer', 'is_staff','is_active')}),
    )
# registering custom user model and admin model
admin.site.register(User,CustomUserAdmin)
