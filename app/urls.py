"""
urls.py - Routes principales du projet

Ce module relie les différentes applications internes du projet Django
(et configure les endpoints d’administration). Il définit les URL
globales et inclut les routes spécifiques de chaque application.
"""

# Importation du module d'administration Django
from django.contrib import admin
# Importation des fonctions pour définir les URLs
from django.urls import path, include

# Liste des routes principales du projet
urlpatterns = [
    # Route pour l'administration Django
    path('admin/', admin.site.urls),

    # Routes pour l'application 'users'
    # Tous les endpoints définis dans users/urls.py seront préfixés par /api/
    path('api/', include('users.urls')),

    # Routes pour l'application 'ecole'
    # Tous les endpoints définis dans ecole/urls.py seront préfixés par /api/
    path('api/', include('ecole.urls')),

    # Routes pour l'application 'files'
    # Tous les endpoints définis dans files/urls.py seront préfixés par /api/files/
    path('api/files/', include('files.urls')),
]
