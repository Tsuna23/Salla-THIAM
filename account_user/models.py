from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # On hash le mot de passe automatiquement
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractBaseUser):
    PROFESSEUR = 'professeur'
    ETUDIANT = 'etudiant'
    
    ROLE_CHOICES = [
        (PROFESSEUR, 'Professeur'),
        (ETUDIANT, 'Étudiant'),
    ]
    
    nom = models.CharField(max_length=150)  # Plus besoin de "unique=True" ici
    email = models.EmailField(unique=True)  # L'email est unique
    password = models.CharField(max_length=255)  # Le mot de passe est stocké ici (haché)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ETUDIANT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Supprime 'nom' et 'role' des REQUIRED_FIELDS # Le champ email est utilisé pour l'authentification

    objects = UtilisateurManager()

    def save(self, *args, **kwargs):
        if not self.pk or not self.password.startswith('pbkdf2_sha256$'):  # S'assurer que le mot de passe est haché si ce n'est pas déjà fait
            self.password = make_password(self.password)  # Hachage du mot de passe
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_name(self):
        return self.nom

    def get_short_name(self):
        return self.nom

    # Méthodes supplémentaires pour les rôles
    def is_professeur(self):
        return self.role == self.PROFESSEUR

    def is_etudiant(self):
        return self.role == self.ETUDIANT
