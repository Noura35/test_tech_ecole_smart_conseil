# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Modèle personnalisé d'utilisateur.

    Hérite de `AbstractUser` et peut être étendu avec des champs supplémentaires.
    Utilisé pour l'authentification et la gestion des comptes.
    """

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
