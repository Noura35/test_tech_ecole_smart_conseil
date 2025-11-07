# users/urls.py
from django.urls import path
from . import views

"""
Définition des routes (endpoints) pour l'application `users` :

Ces routes permettent de gérer l'authentification et l'enregistrement des utilisateurs.
Chaque endpoint est relié à une vue correspondante définie dans users/views.py.
"""

urlpatterns = [
    # Endpoint pour enregistrer un nouvel utilisateur
    # Méthode HTTP : POST
    # URL complète typique : /api/register/
    path('register/', views.register, name='register'),

    # Endpoint pour connecter un utilisateur et obtenir un JWT
    # Méthode HTTP : POST
    # URL complète typique : /api/login/
    path('login/', views.login, name='login'),

    # Endpoint pour déconnecter un utilisateur (blacklist du refresh token)
    # Méthode HTTP : POST
    # URL complète typique : /api/logout/
    path('logout/', views.logout, name='logout'),
]
