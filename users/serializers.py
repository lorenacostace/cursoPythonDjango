# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """
    
    """

    id = serializers.ReadOnlyField()  # Queremos que el user vea su id, pero no que pueda modificarlo, por eso read only
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        """
        Crea una instancia de USer a partir de los datos de validated_data que contiene valores deserializados
        :param validated_data: Diccionario con datos de usuario
        :return: objeto User
        """
        instance = User()

        return self.update(instance, validated_data)


    def update(self, instance, validated_data):
        """
        Actualiza una instancia de User a partir de los datos del diccionario validated_data que contiene valores
        deserializados
        :param instance:
        :param validated_data:
        :return: objeto User actualizado
        """

        # Guardamos los datos de validated_data en nuestro objeto User (instance)
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')

        """
        instance.passwors está mal, xq cuando Django guarda las contraseñas, las guarda encriptadas, por lo que esto no
        nos vale. En vez de eso, usaremos instance.set_password()
        """
        # instance.password = validated_data.get('password')
        instance.set_password(validated_data.get('password'))
        instance.save()  # Para guardar en la base de datos.

        return instance


    def validate_username(self, data):
        """
        Comprobamos si el nombre usuario que intenta registrase ya existe. Si el usuario no exite, devolvemos data, si
        el usuario si existe lanzaremos un excepcion serializers.ValidationError
        """

        # Buscamos un usuario con ese nombre de usuario
        user = User.objects.filter(username=data)

        # Si estoy creando(no hay instancia) comprobar si hay usuarios con ese username
        if not self.instance and len(user) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese username")
        # Si estoy actualizando, el nuevo username es diferente al de la instancia (esta cambiando el username) y
        # existen usuarios ya registrados con el nuevo username
        elif self.instance and self.instance.username != data and len(user) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese username")
        else:
            return data