from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from users.api import UserViewSet

# APIRouter
router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = [
    # API URLS
    url(r'1.0/', include(router.urls)),
]
