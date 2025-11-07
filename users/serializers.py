from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'inscription d'un nouvel utilisateur.

    - Valide le mot de passe selon les règles définies dans Django.
    - Permet de définir le rôle de l'utilisateur ('admin' ou 'user').
    - Sert à créer un utilisateur via l'API REST.
    """

    # Champ mot de passe, uniquement en écriture
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  # validation selon les règles Django
    )

    # Champ rôle avec choix prédéfinis
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default='user'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec les données validées.

        - `username` : nom d'utilisateur obligatoire
        - `email` : email optionnel
        - `password` : mot de passe validé
        - `role` : rôle de l'utilisateur (par défaut 'user')

        Retourne l'instance utilisateur créée.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user
