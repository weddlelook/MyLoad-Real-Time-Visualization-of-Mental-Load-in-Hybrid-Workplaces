from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='myload-start'),
    path('settings/', views.settings, name='myload-settings'),
    path('meeting/', views.start_meeting, name='start-meeting'),
]