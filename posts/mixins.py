from idlelib.debugobj import dispatch

from django.core.exceptions import PermissionDenied
from urllib3 import request


class UserOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.creator != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)