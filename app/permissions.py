from rest_framework.permissions import BasePermission


class GlobalDefaultPermission(BasePermission):
    def has_permission(self, request, view):
        model_permission_codename = self.__get_model_permission_codename(
            method=request.method,
            view=view
        )

        if model_permission_codename is None:
            return False

        return request.user.has_perm(model_permission_codename)

    def __get_model_permission_codename(self, method, view):
        try:
            model = view.queryset.model
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            action = self.__get_action_suffix(method)

            if action is None:
                raise AttributeError('Unsupported HTTP method')

            return f'{app_label}.{action}_{model_name}'
        except AttributeError:
            return None

    def __get_action_suffix(self, method):
        method_action_map = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
            'OPTIONS': 'view',
            'HEAD': 'view',
        }
        return method_action_map.get(method, None)
