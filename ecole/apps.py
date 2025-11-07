"""Configuration de l'application Ecole.

Ce module contient la configuration Django pour l'application de gestion
des écoles. Il définit les paramètres de base comme le type de champ
auto-incrémenté par défaut et le nom de l'application.

Note:
    Cette configuration est automatiquement chargée par Django au démarrage
    de l'application via le fichier `__init__.py`.
"""

from django.apps import AppConfig


class EcoleConfig(AppConfig):
    """Configuration de l'application Ecole.

    Cette classe hérite de `django.apps.AppConfig` et définit les paramètres
    de configuration pour l'application de gestion des écoles.

    Attributes:
        default_auto_field (str): Type de champ utilisé par défaut pour les
            clés primaires auto-générées. Utilise `BigAutoField` pour supporter
            des identifiants jusqu'à 9,223,372,036,854,775,807.
        name (str): Nom de l'application Django. Doit correspondre au nom
            du package Python contenant l'application.

    Example:
        Cette classe est référencée dans `INSTALLED_APPS` de `settings.py`:

        ```python
        INSTALLED_APPS = [
            # ...
            'ecole.apps.EcoleConfig',
            # ...
        ]
        ```

    See Also:
        - Documentation Django AppConfig: https://docs.djangoproject.com/en/stable/ref/applications/
        - BigAutoField: https://docs.djangoproject.com/en/stable/ref/models/fields/#bigautofield
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecole'