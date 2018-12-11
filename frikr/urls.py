from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from photos.api import PhotosViewSet
from photos.views import HomeView, DetailView, CreateView, PhotosListView, UserPhotosView
from users.api import UserViewSet
from users.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


# APIRouter
router = DefaultRouter()
router.register(r'api/1.0/photos', PhotosViewSet)
router.register(r'api/1.0/users', UserViewSet, base_name='user')

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Photos URLs
    url(r'^$', HomeView.as_view(), name='photos_home'),
    url(r'^my-photos/$', login_required(UserPhotosView.as_view()), name='user_photos'),
    url(r'^photos/$', PhotosListView.as_view(), name='photos_list'),
    url(r'^photos/(?P<pk>[0-9]+)$', DetailView.as_view(), name='photo_detail'),
    url(r'^photos/new$', CreateView.as_view(), name='create_photo'),

    # API URLS
    url(r'', include(router.urls)),

    # Users URLs
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),

]
