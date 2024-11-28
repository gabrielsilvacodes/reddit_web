from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Usando a view de login do Django
    path('register/', views.register_view, name='register'),  # Página de registro
    path('profile/', views.ProfileView.as_view(), name='profile'),  # Página de perfil
    path('profile_list/', views.ProfileListView.as_view(), name='profile_list'),  # Lista de perfis
]