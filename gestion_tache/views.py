from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Projet, Tache
from .serializers import ProjetSerializer, TacheSerializer

# recuoerer le model utilisateur
Utilisateur = get_user_model()

# vue pour lister les prohets
class ProjetListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retourne uniquement les projets créés par le professeur connecté"""
        user = self.request.user
        if not user.is_professeur():
            raise PermissionDenied("Vous n'avez pas l'autorisation d'accéder aux projets.")
        return Projet.objects.filter(professeur=user)

    def perform_create(self, serializer):
        """Assigne automatiquement le professeur connecté au projet"""
        user = self.request.user
        if not user.is_professeur():
            raise PermissionDenied("Seuls les professeurs peuvent créer des projets.")
        serializer.save(professeur=user)

#pour recuperer les projet
class ProjetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Seuls les créateurs du projet peuvent voir/modifier leurs projets"""
        user = self.request.user
        return Projet.objects.filter(professeur=user)

# vue pour creer une tache
class TacheListCreateView(generics.ListCreateAPIView):
    serializer_class = TacheSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retourne les tâches du professeur ou celles assignées à un étudiant, filtrées par projet si nécessaire"""
        user = self.request.user
        queryset = Tache.objects.all()

        projet_id = self.request.query_params.get('projet')
        if projet_id:
            queryset = queryset.filter(projet_id=projet_id)

        if user.is_professeur():
            return queryset.filter(projet__professeur=user).select_related('utilisateur')
        return queryset.filter(utilisateur=user).select_related('utilisateur')
    


    def perform_create(self, serializer):
        """Assigne une tâche uniquement à un étudiant"""
        user = self.request.user
        data = self.request.data

        print("🔹 Utilisateur authentifié :", user, "Role :", getattr(user, 'role', 'Non défini'))
        print("📌 Données reçues :", data)

        if not user.is_professeur():
            raise PermissionDenied("Seuls les professeurs peuvent assigner des tâches.")

        # ✅ Vérifier et récupérer le projet
        projet_id = data.get('projet')
        try:
            projet_instance = Projet.objects.get(id=projet_id)
        except Projet.DoesNotExist:
            raise PermissionDenied("Projet non trouvé.")

        # ✅ Vérifier et récupérer l'étudiant
        utilisateur_id = data.get('utilisateur')
        if not utilisateur_id:
            raise PermissionDenied("Un étudiant doit être assigné à la tâche.")

        try:
            utilisateur_instance = Utilisateur.objects.get(id=utilisateur_id)  # ✅ Correction ici
        except Utilisateur.DoesNotExist:
            raise PermissionDenied("L'utilisateur sélectionné n'existe pas.")

        # ✅ Vérifier que ce n'est pas un professeur
        if utilisateur_instance.is_professeur():
            raise PermissionDenied("Vous ne pouvez assigner une tâche qu'à un étudiant.")

        print(f"✅ Création tâche -> Projet: {projet_instance.id}, Étudiant: {utilisateur_instance.nom}")

        # ✅ Sauvegarde de la tâche avec l'étudiant assigné
        serializer.save(projet=projet_instance, utilisateur=utilisateur_instance)

# ✅ Vue pour récupérer, mettre à jour ou supprimer une tâche
class TacheDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TacheSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Restreint l'accès aux tâches du professeur ou de l'étudiant assigné"""
        user = self.request.user
        if user.is_professeur():
            return Tache.objects.filter(projet__professeur=user).select_related('utilisateur')
        return Tache.objects.filter(utilisateur=user).select_related('utilisateur')
