# ai_resume_sorter_django/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # CORRECTED Redirect: Point to the login URL *including* the 'app/' prefix
    path('', lambda request: redirect('app/login/', permanent=False)), # <-- CHANGE THIS LINE

    # Include the sorter app's URLs under the 'app/' prefix
    path('app/', include(('sorter.urls', 'sorter'), namespace='sorter')),
    # Or without namespacing:
    # path('app/', include('sorter.urls')),
]

# Serve uploaded files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)