"""
Mapping for user app.
"""
from django.urls import path

from user.views import *


urlpatterns = [
    path('create/',CreateUserView.as_view()),
    path('token/',CreateTokenView.as_view()),
    path('me/',ManageUserView.as_view()),
]