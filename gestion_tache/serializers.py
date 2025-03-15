from rest_framework import serializers
from .models import Projet, Tache

class ProjetSerializer(serializers.ModelSerializer):
    professeur_nom = serializers.CharField(source='professeur.nom', read_only=True)

    class Meta:
        model = Projet
        fields = ['id', 'titre', 'description', 'date_creation', 'date_limite', 'professeur', 'professeur_nom']
        read_only_fields = ['professeur']

class TacheSerializer(serializers.ModelSerializer):
    projet_titre = serializers.CharField(source='projet.titre', read_only=True)
    utilisateur_nom = serializers.SerializerMethodField()  # ✅ Changer la méthode d'affichage de l'utilisateur

    class Meta:
        model = Tache
        fields = ['id', 'titre', 'description', 'date_limite', 'statut', 'projet', 'projet_titre', 'utilisateur', 'utilisateur_nom','utilisateur_id']

    def get_utilisateur_nom(self, obj):
        """Retourne le nom complet de l'utilisateur assigné"""
        return obj.utilisateur.nom if obj.utilisateur else "Non assigné"

def validate(self, data):
    utilisateur = data.get('utilisateur')
    if utilisateur and utilisateur.is_professeur():
        raise serializers.ValidationError("Un professeur ne peut pas être assigné à une tâche.")
    return data
