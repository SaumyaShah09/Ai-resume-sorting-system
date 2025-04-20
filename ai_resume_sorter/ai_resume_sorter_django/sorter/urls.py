# sorter/urls.py
from django.urls import path
from . import views

app_name = 'sorter' # Keep if you are using namespacing
# sorter/urls.py
# ... other imports ...
app_name = 'sorter'
urlpatterns = [
    # --- Change the Homepage URL path ---
    path('home/', views.home_view, name='home'), # <-- Now at /app/home/
# WRONG: Missing name
path('suggest-title/', views.suggest_title_view),
# CORRECT:
path('suggest-title/', views.suggest_title_view, name='suggest_title'),
    path('download-shortlisted/', views.download_shortlisted, name='download_shortlisted'),
    # --- Existing URLs ---
    path('upload/', views.upload_resume, name='upload_resume'), # <-- Now at /app/upload/
    # ... other paths ...
    path('login/', views.login_view, name='login'),       # <-- Now at /app/login/ (Careful!)
    path('register/', views.register_view, name='register'), # <-- Now at /app/register/ (Careful!)
    path('logout/', views.logout_view, name='logout'),     # <-- Now at /app/logout/ (Careful!)
]