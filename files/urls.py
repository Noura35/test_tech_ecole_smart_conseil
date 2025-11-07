from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet

app_name = 'files'

# -------------------------------------------------------------------
# Router DRF
# -------------------------------------------------------------------
router = DefaultRouter()
router.register(r'', FileViewSet, basename='file')
"""
Router REST Framework pour le module Files.

Endpoints générés automatiquement pour FileViewSet :
- GET    /files/               -> list des fichiers
- POST   /files/               -> création d'un fichier
- GET    /files/{pk}/          -> détail d'un fichier
- PUT    /files/{pk}/          -> mise à jour d'un fichier
- PATCH  /files/{pk}/          -> mise à jour partielle
- DELETE /files/{pk}/          -> suppression d'un fichier
- GET    /files/{pk}/download/ -> téléchargement d'un fichier
- POST   /files/upload_multiple/ -> upload multiple de fichiers
"""

# -------------------------------------------------------------------
# URL patterns
# -------------------------------------------------------------------
urlpatterns = [
    path('', include(router.urls)),
]
"""
URL patterns pour l'app "files".

- Toutes les routes du ViewSet FileViewSet sont incluses via le router DRF.
- `app_name` permet de nommer les routes pour l'utilisation dans les templates et reverse().
"""
