from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from .mixins import *

from .models import *


class BaseView(CartMixin, View):
    def get(self, request):
        products = ProductsForMainPage().get_products('mechmod', 'mod')
        context = {
            'products': products
        }
        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, DetailView):
    MODELS_NAMES_BY_CONTENT_TYPE = {
        'mod': Mod,
        'mechmod': MechMod
    }

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.MODELS_NAMES_BY_CONTENT_TYPE[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ct_model'] = self.model._meta.model_name
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'cart.html', {"cart": self.cart})


class AddToCart(CartMixin, View):
    def get(self, request, *args, **kwargs):
        cont_type = ContentType.objects.get(model=kwargs.get('ct_model'))
        obj_id = cont_type.model_class().objects.get(slug=kwargs.get('product_slug')).id
        cart_product, created = CartProduct.objects.get_or_create(
            cart=self.cart, user=self.cart.owner, content_type=cont_type, object_id=obj_id
        )
        if created:
            self.cart.products.add(cart_product)
        else:
            yet_created = self.cart.products.get(content_type=cont_type, object_id=obj_id)
            yet_created.qty += 1
            yet_created.save()
        self.cart.save()
        # print(a)
        return HttpResponseRedirect('/cart/')


class DeleteFromCart(CartMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('product_slug')
        cont_type = ContentType.objects.get(model=ct_model)
        prod = cont_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            cart=self.cart,user=self.cart.owner,content_type=cont_type,object_id=prod.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        return HttpResponseRedirect('/cart/')
