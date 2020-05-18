import qrcode
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View,TemplateView
from ticket.models import TicketBag,TicketItem
from authentication.forms import UserChangeForm
from django.conf import settings
User = get_user_model()


# Create your views here.

class ProfileView(LoginRequiredMixin, View):
    # renders the profile template
    def get(self, *args, **kwargs):
        return render(self.request, 'profile/profile.html')


class ProfileChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = UserChangeForm(instance=request.user)
        context = {'form': form, }
        return render(self.request, 'profile/update.html', context)

    def post(self, request, *args, **kwargs):
        # creates an instance of the UserChangeForm that can also accepts files
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # if form is valid check to see if the phone number consist of 10 digits
            user_phone = form.cleaned_data.get('phone')
            if len(user_phone) > 10:
                messages.info(request, 'Phone number must be 10 digits')
                return redirect('profile:update')
            form.save()
            messages.success(request, 'You have update your profile')
            # it updates the sessions of the current user 
            update_session_auth_hash(request, request.user)
            return redirect('profile:user_profile')
        context = {'form': form}
        return render(self.request, 'profile/update.html', context)







class UserTickets(TemplateView):
    template_name = 'profile/tickets.html'
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get (self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context["ordered_tickets"] = TicketItem.objects.filter(user=request.user,ordered=True)
        return self.render_to_response(context)
    