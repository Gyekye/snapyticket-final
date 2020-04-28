from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class IndexView(TemplateView):
    template_name = 'core/index.html'
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:home')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)



class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'core/home.html'
    