"""
wsgi.py - Point d’entrée WSGI pour le déploiement du projet Django.

Ce fichier sert de passerelle entre le serveur web (ex: Gunicorn, uWSGI)
et l'application Django. Il permet au serveur de communiquer avec Django
pour traiter les requêtes HTTP.
"""

import os
from django.core.wsgi import get_wsgi_application

# Définir la variable d'environnement pour indiquer le fichier de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Obtenir l'application WSGI de Django
application = get_wsgi_application()
