from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.contrib.auth.models import AnonymousUser
from .models import *


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            # cart = Cart.objects.create(owner=AnonymousUser)
            cart = None
        else:
            cart = Cart.objects.get_or_create(owner=request.user)
        self.cart = cart[0]
        return super().dispatch(request, *args, **kwargs)
