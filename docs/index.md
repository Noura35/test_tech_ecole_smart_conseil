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

## 📚 Navigation

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Installation__

    ---

    Guide d'installation complet pour environnement local et Docker

    [:octicons-arrow-right-24: Guide d'installation](installation/local.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Documentation complète des endpoints REST disponibles

    [:octicons-arrow-right-24: Documentation API](api/authentication.md)

-   :material-book-open-variant:{ .lg .middle } __Guides__

    ---

    Tutoriels et guides pour utiliser l'application

    [:octicons-arrow-right-24: Voir les guides](guides/quickstart.md)

-   :material-code-braces:{ .lg .middle } __Référence__

    ---

    Structure du projet et guide de contribution

    [:octicons-arrow-right-24: Référence technique](reference/structure.md)

</div>

## 🔧 Technologies utilisées

- **Django 4.x** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de données
- **Docker** - Conteneurisation
- **MkDocs Material** - Documentation

## 📄 Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](https://github.com/votre-utilisateur/tech-test/blob/main/LICENSE) pour plus de détails.