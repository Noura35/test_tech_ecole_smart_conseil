from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from ecole.models import Ecole  # Import depuis l'app Ecoles
from .validators import validate_file_size, validate_file_extension
from .utils import get_file_path, determine_file_type, get_mime_type
import os
from django.conf import settings

class File(models.Model):
    """
    Modèle représentant un fichier uploadé dans le système.

    Attributes:
        ecole (ForeignKey): L'école à laquelle le fichier est associé.
        uploaded_by (ForeignKey): L'utilisateur ayant uploadé le fichier.
        file (FileField): Le fichier uploadé.
        filename (str): Nom du fichier.
        file_type (str): Type du fichier (pdf, image, document, etc.).
        file_size (int): Taille du fichier en octets.
        mime_type (str): Type MIME du fichier.
        description (str): Description optionnelle du fichier.
        uploaded_at (datetime): Date et heure de l'upload.
        updated_at (datetime): Date et heure de la dernière modification.
    """

    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('spreadsheet', 'Tableur'),
        ('text', 'Texte'),
        ('other', 'Autre'),
    ]

    # Relations
    ecole = models.ForeignKey(
        Ecole,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name="École"
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='files'
    )

    # Champs fichier
    file = models.FileField(
        upload_to=get_file_path,
        validators=[validate_file_size, validate_file_extension],
        verbose_name="Fichier"
    )

    # Métadonnées
    filename = models.CharField(max_length=255, verbose_name="Nom du fichier")
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default='other')
    file_size = models.IntegerField(verbose_name="Taille (octets)")
    mime_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")

    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Options Meta pour le modèle File."""
        verbose_name = "Fichier"
        verbose_name_plural = "Fichiers"
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['ecole', '-uploaded_at']),
            models.Index(fields=['file_type']),
        ]

    def __str__(self) -> str:
        """
        Représentation en chaîne de caractères d'un fichier.

        Returns:
            str: Nom du fichier suivi du nom de l'école.
        """
        return f"{self.filename} - {self.ecole.name}"

    def save(self, *args, **kwargs):
        """
        Override de la méthode save pour extraire automatiquement les métadonnées
        du fichier uploadé (nom, taille, type et MIME).

        Args:
            *args: Arguments positionnels.
            **kwargs: Arguments nommés.
        """
        if self.file:
            self.filename = os.path.basename(self.file.name)
            self.file_size = self.file.size
            self.file_type = determine_file_type(self.filename)
            self.mime_type = get_mime_type(self.filename)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override de la méthode delete pour supprimer le fichier physique
        du stockage lors de la suppression de l'objet.

        Args:
            *args: Arguments positionnels.
            **kwargs: Arguments nommés.
        """
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def get_file_size_display(self) -> str:
        """
        Retourne la taille du fichier sous une forme lisible par l'utilisateur.

        Returns:
            str: Taille formatée (B, KB ou MB).
        """
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"
