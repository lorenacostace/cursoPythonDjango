# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseNotFound
from photos.form import PhotoForm
from photos.models import Photo, PUBLIC
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db.models import Q


class PhotosQueryset(object):

    def get_photos_queryset(self, request):
        if not request.user.is_authenticated():  # Si el ususario no esta autenticado
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:  # Si el usuario es superadmin
            photos = Photo.objects.all()
        else:  # Utilizamos los operadores a nivel de bit para operar con los objetos Q
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))

        return photos


class HomeView(View):

    def get(self, request):
        # Esta funcion devuelve el home de mi pagina

        photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
        context = {
            'photos_list': photos[:5]
        }

        return render(request, 'photos/home.html', context)


class DetailView(View, PhotosQueryset):

    def get(self, request, pk):
        """
        Carga la pagina de detalle de una foto
        :param request: HttpRequest
        :param pk: id de la foto
        :return: HttpResponse
        """
        """
        Tambien podemos utilizar esta sintaxis para recuperar un objeto:
        try:
            photo = Photos.Objects.get(pk=pk)
        :except Photo.DoesNotExist:
            photo = None
        :except Photo.MultipleObjects
            photo = None
        """

        # Trae la foto con clave pk, y ademas los elementos relacionados
        possible_photos = self.get_photos_queryset(request).filter(pk=pk).select_related('owner')
        photo = possible_photos[0] if len(possible_photos) == 1 else None
        if photo is not None:
            # cargar la plantilla de detalle
            context = {
                'photo': photo
            }
            return render(request, 'photos/detail.html', context)
        else:
            return HttpResponseNotFound('No existe la foto') # 404 Not Found


class CreateView(View):
    """
    method_decorator: es un decorador que decora el decorador login_required. Es necesario usarlo porque login_required
        es un decorador de funciones y no de metodos, por lo que solo no funciona.
    login_required: Es un decorador que evita que sin estar logueado no puedas acceder a crear una foto y redirigir a una URL
    """

    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra un formulario para crear una foto
        :param request: HttpRequest
        :return: HttpResponse
        """

        # Instancio el objeto
        form = PhotoForm()

        context = {
            'form': form,
            'success_message': ''
        }
        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Crea una foto en base a la informacion POST
        :param request: HttpRequest
        :return: HttpResponse
        """
        success_message = ''

        # Instancio el objeto
        photo_with_owner = Photo()

        # Asigno como propietario de la foto, al usuario que esta autenticado
        photo_with_owner.owner = request.user
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            # Guarda el objeto photo y me lo devuelve
            new_photo = form.save()
            form = PhotoForm()
            success_message = 'Guardado con éxito!'
            """No se debe usar new_photo.id, se debe usar pk. pk es la clave primaria que django identifica como id.
                El {0} nos indica el orden en el que van los argumentos
            """
            success_message += '<a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
        context = {
            'form': form,
            'success_message': success_message
        }
        return render(request, 'photos/new_photo.html', context)


class ListView(View, PhotosQueryset):

    def get(self, request):
        """
        Devuelve:
        - Las fotos públicas si el usuario no está autenticado.
        - Las fotos del usuario o publicas si el usuario está autenticado.
        - Si el usuario es superadmin, devuelve todas las fotos.
        :param request: HttpRequest
        :return: HttpRensoponse
        """
        """
        Ejemplo de query que devuelve todas las fotos en las que el autor es Alberto:
        photos = Photo.objects.filter(owner__first_name = 'Alberto')
        """
        context = {
            'photos': self.get_photos_queryset(request)
        }
        return render(request, 'photos/photos_list.html', context)
