from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),
    path('', views.home, name='home'),
    path('<str:short_code>/', views.redirect_url, name='redirect'),
    
    
    path('api/shorten/', views.api_shorten_url, name='api_shorten'),
    # --- New JWT Authentication API Endpoints ---
    # React will POST username/password here to login and get tokens
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # React will send the refresh token here to automatically get a new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # React will POST here to safely log out and destroy the session
    path('api/logout/', views.LogoutView.as_view(), name='auth_logout'),

]