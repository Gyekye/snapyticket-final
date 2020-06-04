from django.urls import path
from .views import HelpCenterView, AboutView, TermsAndConditonsView, PrivacyPolicyView, FaqView, TutorialView

app_name = 'support'

urlpatterns = [
    # url to the main help center page
    path('', HelpCenterView.as_view(), name='help_center'),
    # url to the about us page
    path('about/', AboutView.as_view(), name='about'),
    # url to the privacy policy page
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    # url to the frequently asked questions page
    path('faq/', FaqView.as_view(), name='faq'),
    # url to the how to use qr based tickets page
    path('tutorial/', TutorialView.as_view(), name='tutorial'),
    # url to the terms and conditions page
    path('terms-and-conditons/', TermsAndConditonsView.as_view(), name='terms-and-conditions')
]
