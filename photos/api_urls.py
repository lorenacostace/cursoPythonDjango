# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from photos.api import PhotosViewSet

# APIRouter
router = DefaultRouter()
router.register(r'photos', PhotosViewSet)

urlpatterns = [
    # API URLS
    url(r'1.0/', include(router.urls)),
]
