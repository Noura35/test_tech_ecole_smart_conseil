from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from ecole.models import Ecole
from .models import File

User = get_user_model()


# =====================================================
# Tests unitaires du modèle File
# =====================================================
class FileModelTest(TestCase):
    """Tests unitaires pour le modèle File"""

    def setUp(self):
        """Créer un utilisateur et une école pour les tests"""
        self.user = User.objects.create_user(
            username='admin',
            password='adminpass',
            role='admin',
            is_staff=True
        )
        self.ecole = Ecole.objects.create(
            name="École Alpha",
            address="Rue de la République",
            city="Sousse",
            postal_code="4000",
            phone="12345678",
            students_count=200
        )

    def test_file_creation_with_metadata(self):
        """Test: Création d'un fichier avec extraction automatique des métadonnées.

        Vérifie que les champs filename, file_type, file_size et mime_type
        sont correctement renseignés après la création.

        Asserts:
            - filename correct
            - file_type correct
            - file_size > 0
            - mime_type contient l'extension
        """
        uploaded_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        file_obj = File.objects.create(
            ecole=self.ecole,
            uploaded_by=self.user,
            file=uploaded_file
        )
        self.assertEqual(file_obj.filename, 'test.pdf')
        self.assertEqual(file_obj.file_type, 'pdf')
        self.assertGreater(file_obj.file_size, 0)
        self.assertIn('pdf', file_obj.mime_type)

    def test_file_deletion_removes_physical_file(self):
        """Test: Suppression d'un fichier supprime le fichier physique.

        Vérifie que la suppression de l'objet File supprime également
        le fichier sur le disque.

        Asserts:
            - Le fichier existe avant suppression
            - Le fichier n'existe plus après suppression
        """
        uploaded_file = SimpleUploadedFile("delete_test.pdf", b"content to delete", content_type="application/pdf")
        file_obj = File.objects.create(
            ecole=self.ecole,
            uploaded_by=self.user,
            file=uploaded_file
        )

        file_path = file_obj.file.path
        self.assertTrue(os.path.exists(file_path))

        file_obj.delete()
        self.assertFalse(os.path.exists(file_path))

    def test_file_size_display(self):
        """Test: Formatage lisible de la taille d'un fichier.

        Vérifie que la méthode get_file_size_display retourne une
        chaîne contenant l'unité (B, KB ou MB).

        Asserts:
            - "KB" est présent pour un fichier de 2KB
        """
        uploaded_file = SimpleUploadedFile("size_test.pdf", b"x" * 2048, content_type="application/pdf")
        file_obj = File.objects.create(
            ecole=self.ecole,
            uploaded_by=self.user,
            file=uploaded_file
        )
        size_display = file_obj.get_file_size_display()
        self.assertIn('KB', size_display)


# =====================================================
# Tests API Files
# =====================================================
class FileAPITest(APITestCase):
    """Tests fonctionnels de l'API Files"""

    def setUp(self):
        """Création d'utilisateur et d'écoles pour les tests API"""
        self.user = User.objects.create_user(username='apiuser', password='api123')
        self.client.force_authenticate(user=self.user)
        self.ecole = Ecole.objects.create(
            name='École API',
            address='456 Rue API',
            city='Lyon',
            postal_code='69001',
            phone='0987654321',
            students_count=20
        )
        self.ecole2 = Ecole.objects.create(
            name='École API 2',
            address='789 Rue Test',
            city='Paris',
            postal_code='75001',
            phone='0123456789',
            students_count=30
        )

    def test_upload_file(self):
        """Test: Upload d'un fichier via l'API.

        Vérifie que l'utilisateur authentifié peut uploader un fichier
        et que l'objet File est créé correctement.

        Asserts:
            - Status code 201 Created
            - File count == 1
            - uploaded_by == utilisateur courant
        """
        file = SimpleUploadedFile("upload.pdf", b"content", content_type="application/pdf")
        response = self.client.post(
            '/api/files/',
            {'ecole': self.ecole.id, 'file': file, 'description': 'Test'},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(File.objects.first().uploaded_by, self.user)

    def test_delete_file_admin_only(self):
        """Test: Tentative de suppression par un utilisateur standard.

        Vérifie qu'un utilisateur sans rôle admin ne peut pas supprimer
        un fichier et que celui-ci reste en base.

        Asserts:
            - Status code: 403 Forbidden
            - Le fichier existe toujours en base de données
        """
        file_obj = File.objects.create(
            ecole=self.ecole,
            uploaded_by=self.user,
            file=SimpleUploadedFile("delete.txt", b"content"),
            filename="delete.txt",
            file_size=100
        )
        response = self.client.delete(f'/api/files/{file_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(File.objects.count(), 1)

    def test_delete_file_admin_success(self):
        """Test: Suppression par un utilisateur admin.

        Vérifie qu'un superuser peut supprimer un fichier.

        Asserts:
            - Status code 204 No Content
            - Le fichier est supprimé de la base
        """
        admin_user = User.objects.create_superuser(username='adminuser', password='admin123')
        file_obj = File.objects.create(
            ecole=self.ecole,
            uploaded_by=self.user,
            file=SimpleUploadedFile("delete_admin.txt", b"content"),
            filename="delete_admin.txt",
            file_size=100
        )
        self.client.force_authenticate(user=admin_user)
        response = self.client.delete(f'/api/files/{file_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(File.objects.count(), 0)
