# -*- coding: utf-8 -*-
from photos.models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PhotoListAPI(ListCreateAPIView):
    # Le decimos cual es nuestro modelo y cual es nuestro serializador
    queryset = Photo.objects.all()

    # Para autenticacion
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # Para el detalle de la foto, porque sin esto, el POST no funciona. Dependiendo del método (GET o POST) utilizaremos
    # un serializer u otro.
    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == 'POST' else PhotoListSerializer

    """
    def get(self, request):
    photos = Photo.objects.all()
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data)
    """


class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    # Le decimos cual es nuestro modelo y cual es nuestro serializador
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # Para autenticacion
    permission_classes = (IsAuthenticatedOrReadOnly,)