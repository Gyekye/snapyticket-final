from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .decorators import EventOrganizerRequired
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
# Create your views here.



class DashBoardView(EventOrganizerRequired,View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
