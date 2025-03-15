from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Utilisateur
from .serializers import UtilisateurSerializer
from django.contrib.auth.hashers import make_password

# Serializer personnalisé pour inclure l'email et le rôle dans le token JWT
class TokenObtainPairSerializerWithEmail(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['username'] = attrs.get('email')  # Utilisation de l'email pour la connexion
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['role'] = self.user.role
        return data

# Vue pour générer un token JWT avec l'email et le rôle inclus
class TokenObtainPairViewWithEmail(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializerWithEmail

# Vue pour récupérer les informations de l'utilisateur connecté
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'role': user.role,
            'nom': user.nom,
            'avatar': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
        })


# Vue pour l'inscription des utilisateurs
class UtilisateurListCreateView(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [AllowAny]  # Permet aux nouveaux utilisateurs de s'inscrire

    def create(self, request, *args, **kwargs):
        """Créer un utilisateur avec hachage du mot de passe"""
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)
#vue pour gerer les avatars
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.conf import settings
import os

class AvatarUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        file = request.FILES.get('avatar')

        if not file:
            return Response({'error': 'Aucun fichier reçu'}, status=status.HTTP_400_BAD_REQUEST)

        # Supprime l'ancien avatar s'il existe
        if user.avatar:
            old_avatar_path = os.path.join(settings.MEDIA_ROOT, str(user.avatar))
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)

        # Sauvegarde la nouvelle image
        user.avatar = file
        user.save()

        return Response({'avatar': request.build_absolute_uri(user.avatar.url)}, status=status.HTTP_200_OK)
