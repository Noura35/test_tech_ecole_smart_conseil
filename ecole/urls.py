"""
Définition des routes de l'application **users** liées à la gestion des écoles.

### Détails des Endpoints :

#### 🔹 `GET /ecoles/`
- **Description** : Récupère la liste de toutes les écoles.
- **Accès** : Utilisateurs authentifiés.
- **Réponse (200)** :
```json
  [
    {
      "id": 1,
      "name": "École Nationale d'Informatique",
      "address": "Route de Tunis",
      "city": "Sousse",
      "postal_code": "4000",
      "phone": "+216 73 123 456",
      "students_count": 250,
      "created_at": "2025-11-07T09:12:34Z"
    }
  ]
```

#### 🔹 `POST /ecoles/`
- **Description** : Crée une nouvelle école.
- **Accès** : Réservé aux administrateurs.
- **Exemple de requête** :
```json
  {
    "name": "Institut Supérieur de Technologie",
    "address": "Avenue de la République",
    "city": "Tunis",
    "postal_code": "1002",
    "phone": "+216 71 456 789"
  }
```
- **Réponse (201)** : Détails de l'école créée.

#### 🔹 `GET /ecoles/<int:pk>/`
- **Description** : Récupère les informations d'une école spécifique.
- **Accès** : Utilisateurs authentifiés.

#### 🔹 `PUT /ecoles/<int:pk>/`
- **Description** : Met à jour les informations d'une école existante.
- **Accès** : Réservé aux administrateurs.

#### 🔹 `DELETE /ecoles/<int:pk>/`
- **Description** : Supprime une école.
- **Accès** : Réservé aux administrateurs.
"""

from django.urls import path
from . import views

#: Liste des routes (endpoints) pour la gestion des écoles.
urlpatterns = [
    path(
        'ecoles/',
        views.ecole_list_create,
        name='ecole-list-create'
    ),
    path(
        'ecoles/<int:pk>/',
        views.ecole_detail,
        name='ecole-detail'
    ),
]