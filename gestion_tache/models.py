from django.db import models
from django.conf import settings

class Projet(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateTimeField()
    professeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projets_crees'
    )

    def __str__(self):
        return self.titre

class Tache(models.Model):
    STATUT_CHOICES = [
        ('à faire', 'À faire'),
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_limite = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='à faire')
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='taches'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taches_assignees'
    )

    def __str__(self):
        return self.titre
