from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),  # optional, made path clearer
    path('download-shortlisted/', views.download_shortlisted, name='download_shortlisted'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # 👉 Module 2 paths
    path('suggest-title/', views.suggest_title, name='suggest_title'),
    path('suggested-titles/', views.suggest_title, name='suggested_titles'),

]
