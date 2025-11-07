# Module Users

Le module **Users** gère l’authentification et la gestion des utilisateurs dans le projet Django.  
Il fournit toutes les fonctionnalités nécessaires pour **enregistrer, connecter, déconnecter** les utilisateurs, et gérer leurs rôles.

Le module est structuré en cinq composants principaux : **modèles**, **sérialiseurs**, **vues**, **URLs** et **tests**.

---

## 1. Modèles (`users.models`)

- Définit le modèle `User` personnalisé ou utilise le modèle Django par défaut.  
- Peut inclure des champs supplémentaires tels que `role` pour distinguer les types d’utilisateurs (admin, utilisateur standard, etc.).  
- Sert de base pour l’authentification et la gestion des permissions.  

::: users.models

---

## 2. Sérialiseurs (`users.serializers`)

- Les sérialiseurs transforment les instances de modèle en formats JSON et valident les données entrantes.  
- Exemple :
  - `RegisterSerializer` : validation et création d’un utilisateur lors de l’inscription.  

::: users.serializers

---

## 3. Vues (`users.views`)

Les vues contiennent les **endpoints REST API** pour l’authentification :

| Endpoint      | Méthode | Permissions      | Description |
|---------------|---------|-----------------|-------------|
| `/register/`  | POST    | AllowAny        | Inscription d’un nouvel utilisateur. Retourne un message de succès si l’utilisateur est créé. |
| `/login/`     | POST    | AllowAny        | Connexion d’un utilisateur existant. Retourne un JWT (access + refresh) et les informations de l’utilisateur. |
| `/logout/`    | POST    | IsAuthenticated | Déconnexion d’un utilisateur. Blackliste le refresh token pour sécuriser la session. |

- Utilise **DRF** et **Simple JWT** pour gérer l’authentification et les tokens.  

::: users.views

---

## 4. URLs (`users.urls`)

- Configure le **routing API** pour le module Users.  
- Chaque URL est reliée à sa vue correspondante dans `users.views`.  

::: users.urls

---

## 5. Tests (`users.tests`)

- Contient des **tests unitaires** pour valider le fonctionnement du module Users.  
- Utilise `APITestCase` de DRF pour simuler les requêtes HTTP.  
- Couvre tous les scénarios principaux : inscription, connexion, déconnexion et gestion des tokens.  

::: users.tests

### 5.1. Tableau récapitulatif des tests

| Test                       | Description                                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------------|
| `test_register_user`        | Vérifie l’inscription d’un utilisateur et la création en base.                                |
| `test_login_valid_user`     | Vérifie la connexion d’un utilisateur existant et la génération des JWT.                     |
| `test_login_invalid_user`   | Vérifie le comportement avec des identifiants invalides.                                      |
| `test_logout_valid_token`   | Vérifie la déconnexion avec un refresh token valide (blacklist).                              |
| `test_logout_invalid_token` | Vérifie la gestion des refresh tokens invalides ou déjà utilisés.                             |

