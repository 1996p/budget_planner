from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', AuthenticationView.as_view(), name='login'),
    path('logout/', logout_user, name='logout')
]
