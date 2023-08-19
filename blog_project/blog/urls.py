"""
Mapping for blog API.
"""
from django.urls import path , include

from rest_framework.routers import DefaultRouter

from blog.views import *

router = DefaultRouter()
router.register('blogs',BlogAPIView)
router.register('my_blogs',BlogViewSet)
router.register('my_tags',TagViewSet)

urlpatterns = [
    path('',include(router.urls)),
]