from django.shortcuts import get_object_or_404, render
from django.views.generic import View,TemplateView
from django.http import HttpResponse
from .models import Ticket
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
class TicketView(TemplateView):
    template_name = 'ticket/tickets.html'
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.all()
        return self.render_to_response(context)
    
class TicketDetailView(View):
    def get(self,request,slug,*args,**kwargs):
        # todo #2 add a 404 error if ticket does not exits
        try:
            ticket = Ticket.objects.get(slug__iexact=slug)
        except ObjectDoesNotExist:
            return HttpResponse('Ticket Not Found ')
        return render(request,'ticket/details.html',{'ticket':ticket})
    def post(self, request,slug,*args,**kwargs):
        return HttpResponse('POST request!')