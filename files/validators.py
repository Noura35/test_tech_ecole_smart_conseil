from django.core.exceptions import ValidationError
import os

def validate_file_size(file):
    """
    Valide que la taille d'un fichier ne dépasse pas 10MB.

    Args:
        file (File): Fichier à valider.

    Raises:
        ValidationError: Si la taille du fichier dépasse 10MB.

    Exemple:
        >>> validate_file_size(myfile)
    """
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'La taille du fichier ne doit pas dépasser {max_size_mb}MB')


def validate_file_extension(file):
    """
    Valide que le fichier a une extension autorisée.

    Extensions autorisées :
        - PDF (.pdf)
        - Images (.jpg, .jpeg, .png, .gif)
        - Documents Word (.doc, .docx)
        - Tableurs (.xls, .xlsx, .csv)
        - Texte (.txt)

    Args:
        file (File): Fichier à valider.

    Raises:
        ValidationError: Si l'extension du fichier n'est pas autorisée.

    Exemple:
        >>> validate_file_extension(myfile)
    """
    allowed_extensions = [
        '.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx',
        '.xls', '.xlsx', '.txt', '.csv', '.gif'
    ]
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Extension de fichier non autorisée. Extensions autorisées: {", ".join(allowed_extensions)}'
        )
