from django.urls import path
from .views import DashBoardView,OrganizerUpdate

app_name = 'organizer'

urlpatterns = [
    path('',DashBoardView.as_view(),name='dashboard'),
    path('update/<int:pk>/',OrganizerUpdate.as_view(),name='update'),

]
