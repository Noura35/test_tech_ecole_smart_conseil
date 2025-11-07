from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """
    Configuration de l'administration Django pour le modèle `File`.

    Permet de gérer les fichiers via l'interface admin avec :
    - Affichage des colonnes importantes
    - Filtres par type, date et école
    - Recherche par nom, école et utilisateur
    - Champs en lecture seule pour les métadonnées
    - Organisation en fieldsets pour une meilleure lisibilité
    """

    # Colonnes affichées dans la liste
    list_display = [
        'filename', 'ecole', 'file_type', 'get_file_size_display',
        'uploaded_by', 'uploaded_at'
    ]

    # Filtres disponibles dans la sidebar
    list_filter = ['file_type', 'uploaded_at', 'ecole']

    # Champs sur lesquels la recherche est possible
    search_fields = ['filename', 'ecole__name', 'uploaded_by__username']

    # Champs en lecture seule pour éviter les modifications manuelles
    readonly_fields = [
        'filename', 'file_size', 'file_type', 'mime_type',
        'uploaded_at', 'updated_at'
    ]

    # Organisation des champs dans l'interface d'édition
    fieldsets = (
        ('Informations du fichier', {
            'fields': ('ecole', 'file', 'description')
        }),
        ('Métadonnées', {
            'fields': ('filename', 'file_type', 'file_size', 'mime_type'),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Informations de traçabilité', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
