# -*- coding: utf-8 -*-
from photos.settings import BADWORDS
from django.core.exceptions import ValidationError


def badwords_detector(value):
    """
    Valida si en 'value' se han puesto tacos definidos en settings.BADWORDS
    :return: Boolean
    """

    # Por cada palabra en el settings.BADWORDS, voy a buscar esa palabra dentro de la cadena description, y si
    # existe, lanzo una excepcion. Si no existe, devuelvo los datos limpios/normalizados.
    for badword in BADWORDS:
        if badword.lower() in value.lower():
            raise ValidationError(u'La palabra {0} no esta permitida'.format(badword))

    # Si todo OK, devuelvo True
    return True