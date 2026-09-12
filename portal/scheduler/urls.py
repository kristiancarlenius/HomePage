from django.urls import path

from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('events.json', views.events_json, name='events_json'),
    path('meetings/new/', views.meeting_create, name='meeting_create'),
    path('meetings/<int:pk>/edit/', views.meeting_edit, name='meeting_edit'),
    path('meetings/<int:pk>/delete/', views.meeting_delete, name='meeting_delete'),
]
