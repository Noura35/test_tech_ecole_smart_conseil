"""Tests pour l'API Ecole.

Ce module contient les tests unitaires et d'intégration pour l'API REST
de gestion des écoles. Il teste les permissions, l'authentification JWT,
et les opérations CRUD.

Examples:
    Pour exécuter les tests:

    ```bash
    python manage.py test ecole.tests.test_api
    ```
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ecole.models import Ecole

User = get_user_model()


class EcoleAPITestCase(APITestCase):
    """Tests pour les endpoints de l'API Ecole.

    Cette classe teste l'ensemble des opérations CRUD sur les écoles,
    en vérifiant les permissions basées sur les rôles (admin/user)
    et l'authentification JWT.

    Attributes:
        admin_user (User): Utilisateur avec le rôle admin
        normal_user (User): Utilisateur avec le rôle user standard
        login_url (str): URL de l'endpoint de connexion
        list_create_url (str): URL pour lister/créer des écoles
        ecole (Ecole): Instance d'école créée pour les tests
        detail_url (str): URL pour les opérations sur une école spécifique
    """

    def setUp(self):
        """Configure l'environnement de test.

        Crée deux utilisateurs (admin et user standard) et une école
        de test. Initialise les URLs des endpoints API.
        """
        # Création des utilisateurs
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            role='admin',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='user',
            password='userpass',
            role='user'
        )

        # URLs API
        self.login_url = '/api/login/'
        self.list_create_url = '/api/ecoles/'
        self.ecole = Ecole.objects.create(
            name="École Alpha",
            address="Rue de la République",
            city="Sousse",
            postal_code="4000",
            phone="12345678",
            students_count=200
        )
        self.detail_url = f"/api/ecoles/{self.ecole.id}/"

    def authenticate(self, username, password):
        """Authentifie un utilisateur et configure le header JWT.

        Récupère un token JWT via l'endpoint de login et l'ajoute
        automatiquement au header Authorization pour les requêtes suivantes.

        Args:
            username (str): Nom d'utilisateur
            password (str): Mot de passe

        Note:
            Cette méthode modifie les credentials du client de test
            pour toutes les requêtes suivantes.
        """
        response = self.client.post(self.login_url, {
            "username": username,
            "password": password
        })
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_ecole_list_authenticated(self):
        """Test: Récupération de la liste des écoles (utilisateur authentifié).

        Vérifie qu'un utilisateur authentifié peut récupérer la liste
        complète des écoles.

        Asserts:
            - Status code: 200 OK
            - Nombre d'écoles retournées: 1
        """
        self.authenticate('user', 'userpass')
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_ecole_list_unauthenticated(self):
        """Test: Récupération de la liste sans authentification.

        Vérifie que l'accès à la liste des écoles est refusé
        pour un utilisateur non authentifié.

        Asserts:
            - Status code: 401 Unauthorized ou 403 Forbidden

        Note:
            Django REST Framework peut retourner 401 ou 403 selon
            la configuration des permissions.
        """
        response = self.client.get(self.list_create_url)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
            f"Expected 401 or 403, got {response.status_code}"
        )

    def test_post_ecole_admin(self):
        """Test: Création d'une école par un administrateur.

        Vérifie qu'un utilisateur avec le rôle admin peut créer
        une nouvelle école.

        Asserts:
            - Status code: 201 Created
            - Nombre total d'écoles: 2
        """
        self.authenticate('admin', 'adminpass')
        data = {
            "name": "École Beta",
            "address": "Avenue Habib Bourguiba",
            "city": "Tunis",
            "postal_code": "1000",
            "phone": "99988877",
            "students_count": 150
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ecole.objects.count(), 2)

    def test_post_ecole_non_admin(self):
        """Test: Tentative de création d'une école par un utilisateur standard.

        Vérifie qu'un utilisateur sans rôle admin ne peut pas créer
        de nouvelle école.

        Asserts:
            - Status code: 403 Forbidden
        """
        self.authenticate('user', 'userpass')
        data = {
            "name": "École Gamma",
            "address": "Rue Liberté",
            "city": "Sfax",
            "postal_code": "3000",
            "phone": "77766655",
            "students_count": 100
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_ecole_detail_authenticated(self):
        """Test: Récupération des détails d'une école (utilisateur authentifié).

        Vérifie qu'un utilisateur authentifié peut consulter les détails
        d'une école spécifique.

        Asserts:
            - Status code: 200 OK
            - Nom de l'école: "École Alpha"
        """
        self.authenticate('user', 'userpass')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "École Alpha")

    def test_put_ecole_admin(self):
        """Test: Modification d'une école par un administrateur.

        Vérifie qu'un administrateur peut modifier les informations
        d'une école existante.

        Asserts:
            - Status code: 200 OK
            - Nom modifié: "École Alpha Modifiée"
        """
        self.authenticate('admin', 'adminpass')
        data = {
            "name": "École Alpha Modifiée",
            "address": "Rue République",
            "city": "Sousse",
            "postal_code": "4000",
            "phone": "12345678",
            "students_count": 210
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ecole.refresh_from_db()
        self.assertEqual(self.ecole.name, "École Alpha Modifiée")

    def test_put_ecole_non_admin(self):
        """Test: Tentative de modification par un utilisateur standard.

        Vérifie qu'un utilisateur sans rôle admin ne peut pas modifier
        une école.

        Asserts:
            - Status code: 403 Forbidden
        """
        self.authenticate('user', 'userpass')
        data = {"name": "École Non Autorisée"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ecole_admin(self):
        """Test: Suppression d'une école par un administrateur.

        Vérifie qu'un administrateur peut supprimer une école.

        Asserts:
            - Status code: 204 No Content
            - L'école n'existe plus en base de données
        """
        self.authenticate('admin', 'adminpass')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ecole.objects.filter(id=self.ecole.id).exists())

    def test_delete_ecole_non_admin(self):
        """Test: Tentative de suppression par un utilisateur standard.

        Vérifie qu'un utilisateur sans rôle admin ne peut pas supprimer
        une école et que celle-ci reste en base.

        Asserts:
            - Status code: 403 Forbidden
            - L'école existe toujours en base de données
        """
        self.authenticate('user', 'userpass')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Ecole.objects.filter(id=self.ecole.id).exists())