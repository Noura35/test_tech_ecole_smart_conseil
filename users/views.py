# users/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

# Récupération du modèle User personnalisé ou par défaut de Django
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Endpoint pour enregistrer un nouvel utilisateur.
    Accessible à tous (pas besoin d'authentification).

    Reçoit dans request.data :
        - username : str
        - email : str (optionnel selon le serializer)
        - password : str
        - role : str (optionnel selon le modèle User)

    Retourne :
        - 201 CREATED avec un message de succès si l'utilisateur est créé.
        - 400 BAD REQUEST avec les erreurs du serializer sinon.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Utilisateur créé avec succès ✅"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Endpoint pour connecter un utilisateur et générer un JWT.
    Accessible à tous (pas besoin d'authentification).

    Reçoit dans request.data :
        - username : str
        - password : str

    Processus :
        1. Authentifie l'utilisateur via username/password.
        2. Si authentification réussie :
            - Génère un token JWT (access + refresh).
            - Retourne le username et role de l'utilisateur.
        3. Si échec de l'authentification :
            - Retourne 401 Unauthorized avec message d'erreur.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        # Création d'un token JWT pour l'utilisateur
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "role": user.role,
        })
    return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Endpoint pour déconnecter un utilisateur.
    Nécessite que l'utilisateur soit authentifié (JWT access token).

    Reçoit dans request.data :
        - refresh : str (token JWT de rafraîchissement)

    Processus :
        1. Vérifie la présence du token refresh.
        2. Blackliste le token pour empêcher toute réutilisation.
        3. Retourne un message de succès ou une erreur si le token est invalide.

    Remarque :
        - Utilise la fonctionnalité de blacklist de Simple JWT.
        - Si le token est déjà expiré ou blacklisté, une erreur est renvoyée.
    """
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({"error": "Token manquant"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # Ajout du token à la blacklist
        return Response({"message": "Déconnexion réussie ✅"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        # Peu importe l'erreur (token expiré, invalide ou déjà blacklisté)
        return Response({"error": "Token invalide ou déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)
