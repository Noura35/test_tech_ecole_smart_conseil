# Tech Test

Bienvenue dans la documentation de **Tech Test**, une application Django REST pour la gestion des utilisateurs, écoles et fichiers.

## ✨ Fonctionnalités principales

- 🔐 **Authentification complète** - Inscription, connexion et gestion sécurisée des utilisateurs
- 🏫 **Gestion des écoles** - CRUD complet pour les établissements
- 📁 **Gestion de fichiers** - Upload et gestion de documents
- 🚀 **API REST** - Endpoints documentés et testés
- 🐳 **Docker ready** - Déploiement simplifié avec Docker

## 🚀 Démarrage rapide

=== "Installation locale"
```bash
    git clone https://github.com/Noura35/test_tech_ecole_smart_conseil
    cd tech-test
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    python manage.py migrate
    python manage.py runserver
```

=== "Installation Docker"
```bash
    git clone https://github.com/Noura35/test_tech_ecole_smart_conseil
    cd tech-test
    docker-compose up --build
```

!!! success "Serveur démarré"
    Accédez à l'application sur `http://localhost:8000/` (local) ou `http://localhost:8001/` (Docker)


## 🔧 Technologies utilisées

- **Django 4.x** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de données
- **Docker** - Conteneurisation
- **MkDocs Material** - Documentation

