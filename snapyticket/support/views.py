from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ContactForm
from django.contrib import messages
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

class ContactView(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(self.request, 'support/contact.html', context)

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            form = ContactForm(self.request.POST)
            # checks for form validity
            if form.is_valid():
                # post when verified
                form.save()
                messages.success(self.request, 'Your message has successufully been sent')
                return redirect('support:contact')

            else:
                form.save(commit=False)
                messages.warning(self.request, "Your info couldn't be verified")

        else:
            form = ContactForm()
