from django.urls import path
from .views import (
    ProjetListCreateView,  
    ProjetDetailView,      
    TacheListCreateView,  
    TacheDetailView,       

)

urlpatterns = [
    
    path('projets/', ProjetListCreateView.as_view(), name='projet-list-create'),
    path('projets/<int:pk>/', ProjetDetailView.as_view(), name='projet-detail'),
    path('taches/', TacheListCreateView.as_view(), name='tache-list-create'),
    path('taches/<int:pk>/', TacheDetailView.as_view(), name='tache-detail'),

]