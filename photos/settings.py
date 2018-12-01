# -*- coding: utf-8 -*-
from django.conf import settings #importo el settings del proyecto

COPYRIGHT = 'RIG'
COPYLEFT = 'LEF'
CREATIVE_COMMONS = 'CC'

DEFAULT_LICENSES = (
    (COPYRIGHT, 'Copyright'),
    (COPYLEFT, 'Copyleft'),
    (CREATIVE_COMMONS, 'Creative Commons')
)

"""
getattr funciona igual que el .get de los diccionarios. getattr busca sobre el objeto settings un atributo/variable
llamado LICENSES, y si no lo encuentra, devuelve DEFAULT_LICENSES 
"""
LICENSES = getattr(settings, 'LICENSES', DEFAULT_LICENSES)


""" 
Para poder exportar una variable, utilizamos el getattr. Si la variable no esta definida en el settings de la
aplicacion, cogera el valor por defecto de una lista vacia
"""
BADWORDS = getattr(settings, 'PROJECT_BADWORDS', [])