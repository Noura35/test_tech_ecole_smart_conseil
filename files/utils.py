import os
import mimetypes

def get_file_path(instance, filename):
    """
    Génère le chemin de stockage pour un fichier uploadé.

    Le fichier sera stocké sous :
        schools/{id_ecole}/files/{nom_fichier}

    Args:
        instance (File): Instance du modèle File.
        filename (str): Nom original du fichier.

    Returns:
        str: Chemin relatif où le fichier sera stocké.
    """
    return f'schools/{instance.ecole.id}/files/{filename}'


def determine_file_type(filename):
    """
    Détermine le type de fichier à partir de son extension.

    Les types supportés :
        - PDF
        - Image (jpg, jpeg, png, gif)
        - Document (doc, docx)
        - Tableur (xls, xlsx, csv)
        - Texte (txt)
        - Autre pour les extensions non reconnues

    Args:
        filename (str): Nom du fichier.

    Returns:
        str: Type de fichier ('pdf', 'image', 'document', 'spreadsheet', 'text', 'other').
    """
    ext = os.path.splitext(filename)[1].lower()

    type_mapping = {
        '.pdf': 'pdf',
        '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
        '.doc': 'document', '.docx': 'document',
        '.xls': 'spreadsheet', '.xlsx': 'spreadsheet', '.csv': 'spreadsheet',
        '.txt': 'text',
    }

    return type_mapping.get(ext, 'other')


def get_mime_type(filename):
    """
    Récupère le type MIME d'un fichier.

    Utilise la librairie standard `mimetypes` pour deviner le MIME.
    Si le type ne peut pas être déterminé, retourne 'application/octet-stream'.

    Args:
        filename (str): Nom du fichier.

    Returns:
        str: Type MIME du fichier.
    """
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'application/octet-stream'
