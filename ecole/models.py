from django.db import models

class Ecole(models.Model):
    """Représente une école dans le système de gestion.

    Ce modèle contient les informations principales d'une école,
    telles que son nom, son adresse, sa ville, et le nombre d'étudiants inscrits.

    Attributes:
        name (str): Le nom de l'école.
        address (str): L'adresse complète de l'école.
        city (str): La ville où se trouve l'école.
        postal_code (str): Le code postal de l'école.
        phone (str): Le numéro de téléphone de contact de l'école.
        students_count (int): Le nombre d'étudiants inscrits.
        created_at (datetime): La date de création de l'enregistrement.
    """

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    students_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retourne le nom de l'école sous forme de chaîne."""
        return self.name
