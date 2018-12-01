# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from photos.models import Photo
from photos.settings import BADWORDS


class PhotoForm(forms.ModelForm):
    """
    Formulario para el modelo Photo
    """
    class Meta:
        model = Photo
        exclude = ['owner']

    def clean(self):
        """
        Valida si en la descripcion se han puesto tacos definidos en settings.BADWORDS
        :return: diccionario con los atributos si OK
        """

        # Llamada a super
        cleaned_data = super(PhotoForm, self).clean()

        # Recuperamos el valor de la descripcion del diccionario. Si el valor no existe, devuelve una cadena vacia
        description = cleaned_data.get('description', '')

        """
        Por cada palabra en el settings.BADWORDS, voy a buscar esa palabra dentro de la cadena description, y si
        existe, lanzo una excepcion. Si no existe, devuelvo los datos limpios/normalizados.
        """
        for badword in BADWORDS:
            if badword.lower() in description.lower():
                raise ValidationError(u'La palabra {0} no esta permitida'.format(badword))
