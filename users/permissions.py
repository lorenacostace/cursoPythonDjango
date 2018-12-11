# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la accion(GET, POST, PUT o DELETE)
        """

        # Si quiere crear un usuario, sea quien sea puede
        if view.action == 'create':
            return True
        # Si no es POST, el usuario siempre puede
        elif request.user.is_superuser:
            return True
        # Si es un GET a la vista de detalle, un PUT o un DELETE, tomo la decision en has_object_permission
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        # GET a api/1.0/users
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la accion(GET, PUT o DELETE)
        sobre el objeto obj.
        """
        # Si es superadmin, o el usuario autenticado intenta hacer GET, PUT O DELETE sobre su mismo perfil
        return request.user.is_superuser or request.user == obj