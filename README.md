# Tech Test

Application Django REST pour la gestion des utilisateurs, écoles et fichiers avec authentification complète.

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
  - [Installation locale](#installation-locale)
  - [Installation avec Docker](#installation-avec-docker)
- [API Endpoints](#api-endpoints)
- [Structure du projet](#structure-du-projet)
- [Tests](#tests)
- [Licence](#licence)

## ✨ Fonctionnalités

- Gestion complète des utilisateurs (inscription, connexion, authentification)
- CRUD pour les écoles
- Gestion de fichiers
- API REST documentée
- Authentification sécurisée

## 🔧 Prérequis

- Python 3.8+
- pip
- Git
- Docker et Docker Compose (pour l'installation Docker)

## 🚀 Installation

### Installation locale

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/Noura35/test_tech_ecole_smart_conseil
   cd tech-test
   ```

2. **Créer et activer l'environnement virtuel**
   ```bash
   # Linux / Mac
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   ```
   Éditez le fichier `.env` avec vos paramètres spécifiques.

5. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

6. **Créer un superutilisateur (optionnel)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```
   
   L'application sera accessible sur `http://localhost:8000/`

### Installation avec Docker

1. **Construire et démarrer les conteneurs**
   ```bash
   docker-compose up --build
   ```

2. **Accéder à l'application**
   
   L'application sera accessible sur `http://localhost:8001/`

3. **Commandes utiles**
   
   Entrer dans le conteneur :
   ```bash
   docker-compose exec web bash
   ```
   
   Appliquer les migrations :
   ```bash
   docker-compose exec web python manage.py migrate
   ```
   
   Créer un superutilisateur :
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
   
   Arrêter les conteneurs :
   ```bash
   docker-compose down
   ```

## 🌐 API Endpoints

### Authentification
- `POST /api/register/` - Inscription d'un nouvel utilisateur
- `POST /api/login/` - Connexion utilisateur

### Écoles
- `GET /api/ecoles/` - Liste de toutes les écoles
- `POST /api/ecoles/` - Créer une nouvelle école
- `GET /api/ecoles/<id>/` - Détails d'une école spécifique
- `PUT /api/ecoles/<id>/` - Mettre à jour une école
- `DELETE /api/ecoles/<id>/` - Supprimer une école

### Fichiers
- Endpoints disponibles dans le module `/api/files/`


## 📚 Documentation

Ce projet utilise MkDocs pour générer une documentation interactive.

### Lancer la documentation en local
```bash
# Installation locale
mkdocs serve
```

La documentation sera accessible sur `http://localhost:8000/`

### Avec Docker

Ajoutez ce service dans votre `docker-compose.yml` :
```yaml
  docs:
    build: .
    command: mkdocs serve -a 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8002:8000"
```

Puis lancez :
```bash
docker-compose up docs
```

La documentation sera accessible sur `http://localhost:8002/`

### Générer la documentation statique
```bash
mkdocs build
```

Les fichiers HTML seront générés dans le dossier `site/`.

### Déployer sur GitHub Pages
```bash
mkdocs gh-deploy
```



## 📁 Structure du projet

```
tech-test/
│
├── app/                  # Application principale Django
├── users/                # Module de gestion des utilisateurs
├── ecole/                # Module de gestion des écoles
├── files/                # Module de gestion des fichiers
├── docs/                 # Documentation MkDocs
│   └── index.md          # Page d'accueil de la documentation
├── media/                # Sauvegarder files
├── mkdocs.yml            # Configuration MkDocs
├── manage.py             # Script de gestion Django
├── requirements.txt      # Dépendances Python
├── docker-compose.yml    # Configuration Docker
├── .env.example          # Exemple de variables d'environnement
└── README.md             # Documentation
```

## 🧪 Tests

Pour exécuter la suite de tests complète :

```bash
# Installation locale
python manage.py test

# Avec Docker
docker-compose exec web python manage.py test
```

Pour exécuter les tests d'un module spécifique :
```bash
python manage.py test users
python manage.py test ecole
```


