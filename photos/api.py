# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet
from photos.models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from photos.views import PhotosQueryset


class PhotosViewSet(PhotosQueryset, ModelViewSet):
    # Le decimos cual es nuestro modelo y cual es nuestro serializador
    queryset = Photo.objects.all()

    # Para autenticacion
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Para definir dinamicamente que devolver segun el usuario
        """
        return self.get_photos_queryset(self.request)

    def get_serializer_class(self):
        """
        En funcion del tipo de get que sea (para listar o de detalle) devolvemos un Serializer u otro
        """
        if self.action == 'list':
            return PhotoListSerializer
        else:
            return PhotoSerializer

    def perform_create(self, serializer):
        """
        Sobreescribimos el metodo para que antes de guardar la foto, coja el usuario autenticado y se lo asigne al
        propietario de la foto
        """
        serializer.save(owner=self.request.user)
