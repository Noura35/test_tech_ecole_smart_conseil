from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthTests(APITestCase):
    """
    Suite de tests pour les endpoints d'authentification :
    - Inscription (register)
    - Connexion (login)
    - Déconnexion (logout)
    """

    def setUp(self):
        """
        Initialisation avant chaque test :
        - Définition des URLs pour register, login et logout
        - Préparation des données de test pour un utilisateur
        - Création d'un utilisateur admin pour les tests
        """
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            "username": "noura",
            "password": "strongpassword123",
            "email": "noura@example.com"
        }
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            role="admin"
        )

    def test_register_user(self):
        """
        Test: Inscription d'un nouvel utilisateur.

        Vérifie que l'utilisateur peut être créé via l'endpoint register.

        Asserts:
            - Status code: 201 Created
            - Réponse contient un message de succès
            - L'utilisateur existe dans la base de données
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertTrue(User.objects.filter(username='noura').exists())

    def test_login_valid_user(self):
        """
        Test: Connexion avec un utilisateur valide.

        Vérifie que l'utilisateur existant peut se connecter et obtenir les tokens JWT.

        Asserts:
            - Status code: 200 OK
            - Réponse contient un token 'access'
            - Réponse contient un token 'refresh'
        """
        User.objects.create_user(username="testuser", password="testpass123")
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass123"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_user(self):
        """
        Test: Connexion avec des identifiants invalides.

        Vérifie que l'accès est refusé pour des informations incorrectes.

        Asserts:
            - Status code: 401 Unauthorized
        """
        response = self.client.post(self.login_url, {
            "username": "wrong",
            "password": "wrong"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_valid_token(self):
        """
        Test: Déconnexion avec un refresh token valide.

        Vérifie que l'utilisateur peut se déconnecter et que le refresh token est blacklisté.

        Asserts:
            - Status code: 205 Reset Content
        """
        user = User.objects.create_user(username="logoutuser", password="logoutpass123")
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.post(self.logout_url, {"refresh": str(refresh)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_invalid_token(self):
        """
        Test: Déconnexion avec un refresh token invalide.

        Vérifie que la déconnexion échoue si le refresh token est incorrect ou déjà utilisé.

        Asserts:
            - Status code: 400 Bad Request
        """
        user = User.objects.create_user(username="fakeuser", password="fakepass123")
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.post(self.logout_url, {"refresh": "invalidtoken"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
