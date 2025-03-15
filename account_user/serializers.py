from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from account_user.models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Marque le champ password comme write_only

    class Meta:
        model = Utilisateur
        fields = ['id', 'nom', 'email', 'avatar', 'role', 'password']  # ✅ Ajout de 'id'

    def create(self, validated_data):
        # Hachage du mot de passe avant de créer l'utilisateur
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar:  # Vérifie si un avatar existe
            return request.build_absolute_uri(obj.avatar.url)  # Retourne une URL complète
        return None  # Retourne None si pas d'avatar