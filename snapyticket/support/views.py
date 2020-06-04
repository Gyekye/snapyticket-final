from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class HelpCenterView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'support/help.html')
        
class AboutView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'support/about.html')

class TermsAndConditonsView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'support/terms-and-conditions.html')
        
class PrivacyPolicyView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'support/privacy-policy.html')

class FaqView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'support/faq.html')

class TutorialView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'support/tutorial.html')