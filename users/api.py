# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status  # nos proporciona los codigos HTTP con nombres.
from rest_framework.pagination import PageNumberPagination


# Endpoint del listado
class UserListAPI(APIView):

    def get(self, request):
        # Instancio el paginador
        paginator = PageNumberPagination()

        # Obtengo todos los usuarios
        users = User.objects.all()

        # Paginar el queryset
        paginator.paginate_queryset(users, request)

        # Al serializer le paso lo que quiero serializar. El many=True es para decirle que tiene que serializar mas de
        # un objeto, ya que por defecto, el serializer serializa un objeto.
        serializer = UserSerializer(users, many=True)

        # Guardamos los datos serializados
        serialized_users = serializer.data  # Lista de diccionarios

        """
        Convertimos los datos serializados a JSON. Primero los instanciamos, y despues le decimos que nos renderice los 
        usuarios serializados.
        """
        """
        renderer = JSONRenderer()
        json_users = renderer.render(serialized_users)
        
        return HttpResponse(json_users)
        """

        # Devolvemos la respuesta paginada
        return paginator.get_paginated_response(serialized_users)

    def post(self, request):
        # Le pasamos un diccionario de datos, no una instancia
        serializer = UserSerializer(data=request.data)

        #Valido el serializador
        if serializer.is_valid():
            new_user = serializer.save()

            #devolvemos los datos del usuario creado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Devolvemos el error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Definimos el endpoint de detalle
class UserDetailAPI(APIView):

    def get(self, request, pk):
        #  Buscar el usuario, cuya pk me estan pasando
        user = get_object_or_404(User, pk=pk)

        #Le pasamos el objeto User para que lo serialice, y lo convierta en un diccionario, que guardara en DATA
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request, pk):
        # Debemos comprobar el sl usuario que se desea actualizar existe
        user = get_object_or_404(User, pk=pk)

        # Serializame este usuario(instance=user) con estos datos(data=request.data)
        serializer = UserSerializer(instance=user, data=request.data)

        # Validamos
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Debemos comprobar el sl usuario que se desea actualizar existe
        user = get_object_or_404(User, pk=pk)

        # Borramos el usuario
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)