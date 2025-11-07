from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import File
from ecole.models import Ecole
from .serializers import FileSerializer, FileUploadSerializer, FileListSerializer

class FileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des fichiers.

    Fournit les opérations CRUD standard, ainsi que des actions personnalisées :
    - Télécharger un fichier (`download`)
    - Upload multiple de fichiers (`upload_multiple`)

    Permissions :
    - Authentification requise pour toutes les actions.
    - Seuls les admins peuvent supprimer ou mettre à jour des fichiers.

    Parsing :
    - Supporte MultiPart et Form pour l'upload de fichiers.
    """
    queryset = File.objects.select_related('ecole', 'uploaded_by')
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        """
        Retourne le sérialiseur approprié selon l'action.

        Returns:
            Serializer: Classe de sérialiseur adaptée.
        """
        if self.action == 'list':
            return FileListSerializer
        elif self.action == 'create':
            return FileUploadSerializer
        return FileSerializer

    def get_permissions(self):
        """
        Détermine les permissions selon l'action.

        Returns:
            list: Liste des classes de permissions.
        """
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Retourne le queryset filtré selon les paramètres de requête.

        Query params supportés :
        - `ecole`: Filtrer par ID d'école
        - `type`: Filtrer par type de fichier
        - `my_files`: Si vrai, retourne uniquement les fichiers uploadés par l'utilisateur connecté

        Returns:
            QuerySet: Fichiers filtrés.
        """
        queryset = self.queryset

        ecole_id = self.request.query_params.get('ecole')
        if ecole_id:
            queryset = queryset.filter(ecole_id=ecole_id)

        file_type = self.request.query_params.get('type')
        if file_type:
            queryset = queryset.filter(file_type=file_type)

        my_files = self.request.query_params.get('my_files')
        if my_files:
            queryset = queryset.filter(uploaded_by=self.request.user)

        return queryset

    def perform_create(self, serializer):
        """
        Associe automatiquement l'utilisateur connecté lors de la création d'un fichier.

        Args:
            serializer (Serializer): Sérialiseur validé.
        """
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Télécharger un fichier donné.

        Args:
            request (Request): Requête HTTP
            pk (int): ID du fichier

        Returns:
            FileResponse: Réponse HTTP avec le fichier en pièce jointe.

        Raises:
            Http404: Si le fichier n'existe pas sur le serveur.
        """
        file_obj = self.get_object()
        try:
            response = FileResponse(
                file_obj.file.open('rb'),
                content_type=file_obj.mime_type
            )
            response['Content-Disposition'] = f'attachment; filename="{file_obj.filename}"'
            return response
        except FileNotFoundError:
            raise Http404("Fichier non trouvé sur le serveur")

    @action(detail=False, methods=['post'])
    def upload_multiple(self, request):
        """
        Upload multiple fichiers vers une école spécifique.

        Requête attendue :
        - `ecole`: ID de l'école
        - `files`: Liste de fichiers
        - `description`: Optionnel

        Returns:
            Response: Détails sur les fichiers uploadés et les erreurs éventuelles.
        """
        ecole_id = request.data.get('ecole')
        if not ecole_id:
            return Response({'error': 'ecole_id requis'}, status=status.HTTP_400_BAD_REQUEST)

        school = get_object_or_404(Ecole, pk=ecole_id)
        files = request.FILES.getlist('files')

        if not files:
            return Response({'error': 'Aucun fichier fourni'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_files = []
        errors = []

        for file in files:
            serializer = FileUploadSerializer(data={
                'ecole': school.id,
                'file': file,
                'description': request.data.get('description', '')
            })

            if serializer.is_valid():
                file_obj = serializer.save(uploaded_by=request.user)
                uploaded_files.append(FileSerializer(file_obj, context={'request': request}).data)
            else:
                errors.append({'filename': file.name, 'errors': serializer.errors})

        return Response(
            {
                'uploaded': len(uploaded_files),
                'failed': len(errors),
                'files': uploaded_files,
                'errors': errors
            },
            status=status.HTTP_201_CREATED if uploaded_files else status.HTTP_400_BAD_REQUEST
        )
