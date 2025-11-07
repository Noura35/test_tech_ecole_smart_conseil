# Module Ecole

Le module **Ecole** fournit une **API REST complète** pour la gestion des établissements scolaires, avec :
- Authentification JWT
- Gestion des permissions selon le rôle de l'utilisateur

Le module inclut les composants suivants : **modèles, sérialiseurs, vues, URLs et tests**.

---

## 1. Modèles (`ecole.models`)

- Définit le modèle `Ecole` avec les attributs principaux d’un établissement scolaire.  
- Sert de base pour les opérations CRUD dans l’API.  

::: ecole.models.Ecole

---

## 2. Sérialiseurs (`ecole.serializers`)

- Transforme les instances du modèle `Ecole` en JSON et valide les données entrantes.  
- Exemple :
  - `EcoleSerializer` : sérialiseur principal pour créer et mettre à jour les écoles.  

::: ecole.serializers.EcoleSerializer

---

## 3. Vues (`ecole.views`)

- Les vues utilisent les décorateurs DRF pour gérer **authentification, permissions et routing**.  
- Endpoints principaux :

| Vue                        | Description                              |
|-----------------------------|------------------------------------------|
| `ecole_list_create`         | Liste toutes les écoles ou crée une nouvelle école |
| `ecole_detail`              | Détails, modification ou suppression d’une école |

::: ecole.views.ecole_list_create
::: ecole.views.ecole_detail

---

## 4. URLs (`ecole.urls`)

- Configure le routing API pour le module Ecole.  
- Routes disponibles :

| Méthode HTTP | Endpoint           | Description                  | Permission requise       |
|--------------|------------------|------------------------------|------------------------|
| GET          | /api/ecoles/      | Liste toutes les écoles      | Utilisateur authentifié |
| POST         | /api/ecoles/      | Crée une nouvelle école     | Administrateur          |
| GET          | /api/ecoles/{id}/ | Détails d'une école         | Utilisateur authentifié |
| PUT          | /api/ecoles/{id}/ | Modifie une école complète  | Administrateur          |
| PATCH        | /api/ecoles/{id}/ | Modification partielle      | Administrateur          |
| DELETE       | /api/ecoles/{id}/ | Supprime une école          | Administrateur          |

::: ecole.urls

---

## 5. Tests (`ecole.tests`)

- Suite de **tests unitaires complète** couvrant toutes les opérations CRUD avec différents niveaux de permissions.  
- Vérifie les **scénarios de succès et d’échec** selon le rôle de l’utilisateur (admin ou standard).  

### 5.1. Tableau récapitulatif des tests CRUD

| Test                           | Méthode | Rôle       | Résultat attendu      |
|--------------------------------|---------|-----------|--------------------|
| `test_get_ecole_list_authenticated`   | GET     | user      | 200 OK             |
| `test_get_ecole_list_unauthenticated` | GET     | anonyme   | 401/403            |
| `test_get_ecole_detail_authenticated` | GET     | user      | 200 OK             |
| `test_post_ecole_admin`               | POST    | admin     | 201 Created        |
| `test_post_ecole_non_admin`           | POST    | user      | 403 Forbidden      |
| `test_put_ecole_admin`                | PUT     | admin     | 200 OK             |
| `test_put_ecole_non_admin`            | PUT     | user      | 403 Forbidden      |
| `test_delete_ecole_admin`             | DELETE  | admin     | 204 No Content     |
| `test_delete_ecole_non_admin`         | DELETE  | user      | 403 Forbidden      |

### 5.2. Notes sur les tests

- Les tests vérifient **l’authentification, les permissions et les réponses HTTP** pour chaque endpoint.  
- Permet de garantir que seuls les utilisateurs autorisés (admin) peuvent créer, modifier ou supprimer une école, tandis que les utilisateurs standards ne peuvent que consulter les données.

