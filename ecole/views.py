from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Ecole
from .serializers import EcoleSerializer


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def ecole_list_create(request):
    """
    Liste et création d'écoles.

    ### Méthodes disponibles :
    - **GET** : Récupère la liste de toutes les écoles.
    - **POST** : Crée une nouvelle école (réservé aux administrateurs).

    ### Conditions d'accès :
    - L'utilisateur doit être authentifié.
    - La création (`POST`) nécessite que l'utilisateur soit administrateur (`is_staff=True` ou `role='admin'`).

    ### Réponses :
    - **200 OK** : Retourne la liste des écoles (GET).
    - **201 CREATED** : Retourne les détails de l’école créée (POST réussi).
    - **403 FORBIDDEN** : Si un utilisateur non-admin tente de créer une école.
    - **400 BAD REQUEST** : Si les données fournies sont invalides.

    ### Exemple de requête POST :
    ```json
    {
        "name": "École Nationale d'Informatique",
        "address": "Route de Tunis",
        "city": "Sousse",
        "postal_code": "4000",
        "phone": "+216 73 123 456"
    }
    ```

    ### Exemple de réponse (GET) :
    ```json
    [
        {
            "id": 1,
            "name": "École Nationale d'Informatique",
            "address": "Route de Tunis",
            "city": "Sousse",
            "postal_code": "4000",
            "phone": "+216 73 123 456",
            "students_count": 250,
            "created_at": "2025-11-07T09:12:34Z"
        }
    ]
    ```
    """
    if request.method == 'GET':
        ecoles = Ecole.objects.all()
        serializer = EcoleSerializer(ecoles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_staff and getattr(request.user, "role", "") != 'admin':
            return Response(
                {"error": "Seul un administrateur peut créer une école."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = EcoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def ecole_detail(request, pk):
    """
    Consultation, mise à jour ou suppression d'une école spécifique.

    ### Méthodes disponibles :
    - **GET** : Récupère les détails d’une école spécifique.
    - **PUT** : Met à jour les informations d’une école (réservé aux administrateurs).
    - **DELETE** : Supprime une école (réservé aux administrateurs).

    ### Paramètres :
    - `pk` *(int)* : Identifiant unique de l’école.

    ### Conditions d'accès :
    - L'utilisateur doit être authentifié.
    - Les opérations PUT et DELETE sont réservées aux administrateurs.

    ### Réponses :
    - **200 OK** : Retourne les détails de l’école (GET ou PUT réussi).
    - **204 NO CONTENT** : Confirme la suppression réussie.
    - **403 FORBIDDEN** : Si un utilisateur non-admin tente de modifier/supprimer.
    - **404 NOT FOUND** : Si l’école demandée n’existe pas.
    - **400 BAD REQUEST** : Si les données envoyées lors de la mise à jour sont invalides.

    ### Exemple de réponse (GET) :
    ```json
    {
        "id": 2,
        "name": "Institut Supérieur de Technologie",
        "address": "Avenue de la République",
        "city": "Tunis",
        "postal_code": "1002",
        "phone": "+216 71 456 789",
        "students_count": 120,
        "created_at": "2025-10-30T14:30:00Z"
    }
    ```
    """
    try:
        ecole = Ecole.objects.get(pk=pk)
    except Ecole.DoesNotExist:
        return Response({'error': 'École non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EcoleSerializer(ecole)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.is_staff and getattr(request.user, "role", "") != 'admin':
            return Response(
                {"error": "Seul un administrateur peut modifier une école."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = EcoleSerializer(ecole, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_staff and getattr(request.user, "role", "") != 'admin':
            return Response(
                {"error": "Seul un administrateur peut supprimer une école."},
                status=status.HTTP_403_FORBIDDEN
            )
        ecole.delete()
        return Response({'message': 'École supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
