from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect  # 👈 added for root redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login/')),  # 👈 root redirects to login
    path('', include('sorter.urls')),              # your app urls
]

# Serve uploaded files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
