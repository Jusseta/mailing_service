from django.urls import path
from users.apps import UsersConfig
from users.views import *


app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_<str:key>/', verify, name='verify'),
]
