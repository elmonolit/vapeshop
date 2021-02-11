from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.contrib.auth.models import AnonymousUser
from .models import *


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            # cart = Cart.objects.create(owner=AnonymousUser)
            return super().dispatch(request, *args, **kwargs)

        else:
            cart = Cart.objects.get_or_create(owner=request.user)

        self.cart = cart[0]
        self.cart.total_products = len(self.cart.products.all())
        self.cart.final_price = sum((product.final_price for product in self.cart.products.all()))
        self.cart.save()
        return super().dispatch(request, *args, **kwargs)

    def content_type_get_or_create(self, kwargs):
        cont_type = ContentType.objects.get(model=kwargs.get('ct_model'))
        obj_id = cont_type.model_class().objects.get(slug=kwargs.get('product_slug')).id
        cart_product, created = CartProduct.objects.get_or_create(
            cart=self.cart, user=self.cart.owner, content_type=cont_type, object_id=obj_id
        )
        return cont_type, obj_id, cart_product, created


