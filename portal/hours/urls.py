from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_hours, name='my_hours'),
    path('new/', views.entry_create, name='entry_create'),
    path('<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('billing/', views.billing, name='billing'),
    path('billing/export.csv', views.billing_csv, name='billing_csv'),
]
