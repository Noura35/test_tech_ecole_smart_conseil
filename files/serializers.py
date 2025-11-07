from rest_framework import serializers
from .models import File
from ecole.models import Ecole

class FileSerializer(serializers.ModelSerializer):
    """
    Sérialiseur complet pour le modèle `File`.

    Fournit toutes les informations détaillées du fichier, y compris :
    - Nom de l'utilisateur ayant uploadé le fichier
    - Nom de l'école
    - Taille formatée
    - URL complète du fichier
    """
    uploaded_by_username = serializers.CharField(
        source='uploaded_by.username',
        read_only=True
    )
    ecole_name = serializers.CharField(
        source='ecole.name',
        read_only=True
    )
    file_size_display = serializers.CharField(
        source='get_file_size_display',
        read_only=True
    )
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            'id', 'ecole', 'ecole_name', 'file', 'file_url', 'filename',
            'file_type', 'file_size', 'file_size_display', 'mime_type',
            'description', 'uploaded_by', 'uploaded_by_username',
            'uploaded_at', 'updated_at'
        ]
        read_only_fields = [
            'filename', 'file_size', 'file_type', 'mime_type',
            'uploaded_by', 'uploaded_at', 'updated_at'
        ]

    def get_file_url(self, obj):
        """
        Retourne l'URL complète du fichier.

        Args:
            obj (File): Instance du modèle `File`.

        Returns:
            str | None: URL complète du fichier si disponible, sinon None.
        """
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class FileUploadSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'upload de fichiers.

    Se limite aux champs nécessaires pour créer un nouveau fichier :
    - ecole
    - file
    - description
    """
    class Meta:
        model = File
        fields = ['ecole', 'file', 'description']

    def validate_ecole(self, value):
        """
        Vérifie que l'école existe dans la base de données.

        Args:
            value (Ecole): Instance de l'école.

        Raises:
            serializers.ValidationError: Si l'école n'existe pas.

        Returns:
            Ecole: L'école validée.
        """
        if not Ecole.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("École non trouvée")
        return value


class FileListSerializer(serializers.ModelSerializer):
    """
    Sérialiseur léger pour lister les fichiers.

    Fournit uniquement les informations essentielles pour les listes ou aperçus :
    - Nom du fichier
    - Type
    - Taille
    - Nom de l'école
    - Nom de l'utilisateur ayant uploadé
    - Date de création
    """
    ecole_name = serializers.CharField(
        source='ecole.name',
        read_only=True
    )
    uploaded_by_username = serializers.CharField(
        source='uploaded_by.username',
        read_only=True
    )

    class Meta:
        model = File
        fields = [
            'id', 'filename', 'file_type', 'file_size',
            'ecole', 'ecole_name', 'uploaded_by_username', 'uploaded_at'
        ]
