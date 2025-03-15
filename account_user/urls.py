from django.urls import path
from .views import UtilisateurListCreateView, TokenObtainPairViewWithEmail, UserInfoView, AvatarUploadView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
   
    path('user/', UtilisateurListCreateView.as_view(), name='utilisateur-list'),
    path('token/', TokenObtainPairViewWithEmail.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
     path('upload-avatar/', AvatarUploadView.as_view(), name='upload-avatar'),
]