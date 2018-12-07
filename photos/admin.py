# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from photos.models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_name', 'license', 'visibility')
    list_filter = ('license', 'visibility')
    search_fields = ('name', 'description')

    def owner_name(self, obj):
        return obj.owner.first_name + u' ' + obj.owner.last_name
    owner_name.short_description = u'Photo owner'
    owner_name.admin_order_field = 'owner' # paraa ordenar los datos

    fieldsets = (
        (None, {
            'fields': ('name',),  # Si no se pone la coma después de 'name', python no detecta que es una tupla
            'classes': ('wide',)  # la clase wide alinea los campos
        }),  # Esta coma es importante, sino la ponemos,el analizador sintáctico de python no detectará que es una tupla
        ('Description & Author', {
            'fields': ('description', 'owner'),
            'classes': ('wide',)
        }),
        ('Extra', {
            'fields': ('url', 'license', 'visibility'),
            'classes': ('wide', 'collapse')  # La clase collapse permite mostrar/esconder esa parte
        })
    )

admin.site.register(Photo, PhotoAdmin)
