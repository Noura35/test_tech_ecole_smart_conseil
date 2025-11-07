from django.db.models import fields
from rest_framework import serializers
from .models import Ecole
import re


class EcoleSerializer(serializers.ModelSerializer):
    """
    Le EcoleSerializer gère la sérialisation/désérialisation des données et la validation des champs.

    Ce sérialiseur gère la conversion des instances du modèle Ecole en JSON
    et vice-versa pour les opérations CRUD via l'API REST.

    Attributes:
        name (str): Nom de l'école (requis, max 255 caractères).
        address (str): Adresse complète de l'école (requis).
        city (str): Ville où se situe l'école (requis, max 100 caractères).
        postal_code (str): Code postal de l'école (requis, format: 4 chiffres).
        phone (str): Numéro de téléphone au format international (requis).
        students_count (int): Nombre total d'étudiants inscrits (lecture seule).

    Validation:
        - Le nom de l'école doit être unique.
        - Le code postal doit contenir exactement 4 chiffres.
        - Le numéro de téléphone doit suivre le format international (+216...).

"""


    # Champ calculé en lecture seule
    students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ecole
        fields = ('id', 'name', 'address', 'city', 'postal_code', 'phone', 'students_count')
        read_only_fields = ('id', 'students_count')

    def validate_postal_code(self, value):
        """
        Valide le format du code postal tunisien.

        Args:
            value (str): Le code postal à valider.

        Returns:
            str: Le code postal validé.

        Raises:
            ValidationError: Si le code postal n'est pas composé de 4 chiffres.
        """
        if not re.match(r'^\d{4}$', value):
            raise serializers.ValidationError(
                "Le code postal doit contenir exactement 4 chiffres."
            )
        return value

    def validate_phone(self, value):
        """
        Valide le format du numéro de téléphone.

        Args:
            value (str): Le numéro de téléphone à valider.

        Returns:
            str: Le numéro de téléphone validé.

        Raises:
            ValidationError: Si le format du téléphone est invalide.
        """
        # Format attendu: +216 XX XXX XXX
        phone_pattern = r'^\+216\s?\d{2}\s?\d{3}\s?\d{3,4}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError(
                "Le numéro de téléphone doit être au format international (+216 XX XXX XXX)."
            )
        return value

    def validate_name(self, value):
        """
        Valide le nom de l'école.

        Args:
            value (str): Le nom de l'école à valider.

        Returns:
            str: Le nom validé.

        Raises:
            ValidationError: Si le nom est trop court.
        """
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Le nom de l'école doit contenir au moins 3 caractères."
            )
        return value.strip()

    def validate(self, data):
        """
        Validation globale des données de l'école.

        Args:
            data (dict): Données à valider.

        Returns:
            dict: Données validées.

        Raises:
            ValidationError: Si les données ne sont pas cohérentes.
        """
        # Validation supplémentaire si nécessaire
        return data

    def create(self, validated_data):
        """
        Crée et retourne une nouvelle instance d'Ecole.

        Args:
            validated_data (dict): Données validées pour créer l'école.

        Returns:
            Ecole: L'instance de l'école créée.
        """
        return Ecole.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Met à jour et retourne une instance d'Ecole existante.

        Args:
            instance (Ecole): L'instance existante à mettre à jour.
            validated_data (dict): Nouvelles données validées.

        Returns:
            Ecole: L'instance mise à jour.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance