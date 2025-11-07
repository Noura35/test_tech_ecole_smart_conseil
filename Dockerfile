# Utilise l'image officielle Python 3.12 slim
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port de l'application
EXPOSE 8000

# Commande par défaut pour démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
