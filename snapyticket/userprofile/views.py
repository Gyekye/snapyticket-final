import qrcode
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View,TemplateView
from ticket.models import TicketBag,TicketItem
from authentication.forms import UserChangeForm
from django.conf import settings
from django.db.models import ObjectDoesNotExist

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
        #* creates an instance of the UserChangeForm that can also accepts files
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have update your profile')
            #* it updates the sessions of the current user 
            update_session_auth_hash(request, request.user)
            return redirect('profile:user_profile')
        context = {'form': form}
        return render(self.request, 'profile/update.html', context)
    
    
class UserTicketsList(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            user_ticket_bag = TicketBag.ordered_ticket_bags.filter(
                user=request.user,
                ordered=True
                ).order_by('-created_on')
        except ObjectDoesNotExist:
            messages.success(request,'You have not bought any ticket yet')
            return redirect('core:home')
        context = {'ordered_ticket_bag':user_ticket_bag}
        return render(request,'profile/tickets.html',context)


class UserAllTicketsList(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            all_tickets = TicketItem.objects.filter(
                user=request.user,
                ordered=True
                )
        except ObjectDoesNotExist:
            messages.success(request,'You have not bought any ticket yet')
            return redirect('core:home')
        context = {'all_tickets':all_tickets}
        return render(request,'profile/all-tickets.html',context)
    
        
class UserTicketsDetail(LoginRequiredMixin,View):
    def get(self, request,order_ref_code,*args, **kwargs):
        try:
            user_ticket_bag = TicketBag.ordered_ticket_bags.get(
                order_ref_code=order_ref_code,
                user=request.user
                )
        except ObjectDoesNotExist:
            messages.success(request,'You have not bought any ticket yet')
            return redirect('core:home')
        context = {'ordered_ticket_bag':user_ticket_bag}
        return render(request,'profile/ticket-details.html',context)
        

