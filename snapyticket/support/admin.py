from django.contrib import admin
from .models import *


class MemberSocialProfileInline(admin.TabularInline):
    min_num = 1
    model = SocialProfile
    fields = ['social_platform','profile_url']
    
    
class OurTeamAdmin(admin.ModelAdmin):
    inlines = [MemberSocialProfileInline]
    list_display = [
        'first_name',
        'last_name',
        'role',
        'image',
    ]
    
    
admin.site.register(TermsAndCondition)


admin.site.register(PrivacyPolicy)


admin.site.register(OurTeam,OurTeamAdmin)