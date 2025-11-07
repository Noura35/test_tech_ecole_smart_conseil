"""
asgi.py - Point d’entrée ASGI pour le déploiement asynchrone du projet Django.

Ce fichier sert de passerelle entre le serveur ASGI (ex: Daphne, Uvicorn)
et l'application Django. Il permet la gestion des requêtes asynchrones,
y compris WebSockets et HTTP, pour un traitement non bloquant.
"""

import os
from django.core.asgi import get_asgi_application

# Définir la variable d'environnement pour indiquer le fichier de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Obtenir l'application ASGI de Django
application = get_asgi_application()
