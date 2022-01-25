"""
authapp namespace url configuration
"""

from django.urls import path
import authapp.views as authapp

app_name = 'authapp'
urlpatterns = [
    path('login/', authapp.UserLogin.as_view(), name='login'),
    path('register/', authapp.UserRegister.as_view(), name='register'),
    path('verification/<str:email>/<str:activation_key>/', authapp.user_verification, name='verification'),
    path('logout/', authapp.UserLogout.as_view(), name='logout'),
    path('profile/', authapp.UserInfo.as_view(), name='profile'),
]
