# Module App

Le module **App** contient la configuration principale du projet Django et gère le routage global, ainsi que les interfaces ASGI/WSGI.

---

## 1. Fichier `settings.py`

- Contient **toutes les configurations du projet** :
  - Applications installées
  - Middleware
  - Configuration de la base de données
  - Gestion des templates et statics
  - Paramètres de sécurité
  - Configuration des JWT et DRF  

::: app.settings

---

## 2. Fichier `urls.py`

- Configure le **routing global du projet**, incluant :
  - Les routes des applications internes (`users`, `ecole`, etc.)
  - Les endpoints d’API  
- Sert de point d’entrée pour toutes les requêtes HTTP.  

::: app.urls

---

## 3. Fichier `asgi.py`

- Point d’entrée ASGI pour le projet.
- Gère les communications **asynchrones** (WebSockets, HTTP/2, etc.) si utilisées.
- Permet le déploiement sur des serveurs ASGI comme Daphne ou Uvicorn.  

::: app.asgi

---

## 4. Fichier `wsgi.py`

- Point d’entrée WSGI pour le projet.
- Utilisé pour le déploiement sur des serveurs WSGI classiques (Gunicorn, uWSGI).
- Sert à gérer les requêtes HTTP synchrones.  

::: app.wsgi
