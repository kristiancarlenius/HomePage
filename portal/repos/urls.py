from django.urls import path

from . import views

urlpatterns = [
    path('', views.repo_list, name='repo_list'),
    path('new/', views.repo_create, name='repo_create'),
    path('<int:pk>/edit/', views.repo_edit, name='repo_edit'),
    path('<int:pk>/delete/', views.repo_delete, name='repo_delete'),
]
