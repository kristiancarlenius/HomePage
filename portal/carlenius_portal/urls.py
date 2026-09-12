from django.contrib import admin
from django.urls import include, path

# everything sits under /app/ so nginx can proxy it as one block
urlpatterns = [
    path('app/admin/', admin.site.urls),
    path('app/calendar/', include('scheduler.urls')),
    path('app/customers/', include('customers.urls')),
    path('app/hours/', include('hours.urls')),
    path('app/repos/', include('repos.urls')),
    path('app/', include('accounts.urls')),
]
