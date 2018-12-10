# -*- coding: utf-8 -*-
from photos.models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from photos.views import PhotosQueryset


class PhotoListAPI(PhotosQueryset, ListCreateAPIView):
    # Le decimos cual es nuestro modelo y cual es nuestro serializador
    queryset = Photo.objects.all()

    # Para autenticacion
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # Para el detalle de la foto, porque sin esto, el POST no funciona. Dependiendo del método (GET o POST) utilizaremos
    # un serializer u otro.
    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == 'POST' else PhotoListSerializer

    # Para definir dinamicamente que devolver segun el usuario
    def get_queryset(self):
        return self.get_photos_queryset(self.request)


    """
    def get(self, request):
    photos = Photo.objects.all()
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data)
    """


class PhotoDetailAPI(PhotosQueryset, RetrieveUpdateDestroyAPIView):
    # Le decimos cual es nuestro modelo y cual es nuestro serializador
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # Para autenticacion
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # Para definir dinamicamente que devolver segun el usuario
    def get_queryset(self):
        return self.get_photos_queryset(self.request)