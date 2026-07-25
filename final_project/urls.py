from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from notes import views as notes_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='notes/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', notes_views.register, name='register'),
    path('', include('notes.urls')),
]