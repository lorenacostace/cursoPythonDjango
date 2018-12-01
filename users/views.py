# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout, authenticate, login as django_login
from users.forms import LoginForm
from django.views.generic import View

class LoginView(View):
    def get(self, request):
        error_messages = []
        form = LoginForm()

        #Es necesario el context para pasarle a la plantilla los mensajes
        context = {
            'errors': error_messages,
            'login_form': form
        }

        return render(request, 'users/login.html', context)

    def post(self, request):
        error_messages = []
        
        # Instancio el objeto
        form = LoginForm(request.POST)

        #Caso en el que el formulario es válido
        if form.is_valid():
            #Recuperamos el nombre de usuario y contraseña que ha introducido el usuario
            username = form.cleaned_data.get('usr') #cleaned_data es el atributo con los datos limpios (espacios, etc..)
            password = form.cleaned_data.get('pwd')

            #Obtenemos un objeto user en funcion de los parametros pasados
            user = authenticate(username=username, password=password)

            if user is None:
                error_messages.append('Nombre de usuario o contraseña incorrectos')
            else:
                #Comprobamos si el usuario está activo, ya que en django hay varios estados
                if user.is_active:
                    django_login(request, user)
                    url = request.GET.get('next', 'photos_home')
                    return redirect(url)
                else:
                    error_messages.append('El usuario no está activo')

        #Es necesario el context para pasarle a la plantilla los mensajes
        context = {
            'errors': error_messages,
            'login_form': form
        }

        return render(request, 'users/login.html', context)

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            django_logout(request)
        return redirect('photos_home')