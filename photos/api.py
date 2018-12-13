# -*- coding: utf-8 -*-
from rest_framework.filters import SearchFilter, OrderingFilter
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

    # Le decimos cuales son los backends de filtrado. SearcFilter para búsqueda, y OrderingFilter para filtrado.
    filter_backends = (SearchFilter, OrderingFilter)

    # Campos de búsqueda
    search_fields = ('name', 'description', 'owner__first_name')

    # Ordenamos por nombre y propietario
    ordering_fields = ('name', 'owner')

    def get_queryset(self):
        """
        Para definir dinámicamente que devolver segun el usuario
        """
        return self.get_photos_queryset(self.request)

    def get_serializer_class(self):
        """
        En función del tipo de get que sea (para listar o de detalle) devolvemos un Serializer u otro
        """
        if self.action == 'list':
            return PhotoListSerializer
        else:
            return PhotoSerializer

    def perform_create(self, serializer):
        """
        Sobreescribimos el método para que antes de guardar la foto, coja el usuario autenticado y se lo asigne al
        propietario de la foto
        """
        serializer.save(owner=self.request.user)
