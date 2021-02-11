from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView, CreateView
from django.contrib import messages

from .mixins import *
from .models import *
from .forms import *


class BaseView(CartMixin, View):
    def get(self, request):
        products = ProductsForMainPage().get_products('mechmod', 'mod')
        context = {
            'products': products,
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
        cont_type, obj_id, cart_product, created = self.content_type_get_or_create(kwargs)
        if created:
            self.cart.products.add(cart_product)
        else:
            yet_created = self.cart.products.get(content_type=cont_type, object_id=obj_id)
            yet_created.qty += 1
            yet_created.save()
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class DeleteFromCart(CartMixin, View):
    def get(self, request, *args, **kwargs):
        cart_product = self.content_type_get_or_create(kwargs)[2]
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        messages.add_message(request, messages.WARNING, 'Товар удален из корзины')
        return HttpResponseRedirect('/cart/')


class ChangeQTY(CartMixin, View):
    def post(self, request, *args, **kwargs):
        cart_product = self.content_type_get_or_create(kwargs)[2]
        cart_product.qty = int(request.POST.get('qty'))
        cart_product.save()
        messages.add_message(request, messages.SUCCESS, 'Вы успешно изменили количество товара')
        return HttpResponseRedirect('/cart/')


class OrderView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = OrderForm()
        return render(request, 'order.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.cart = self.cart
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Вы успешно оформили заказ')
            return HttpResponseRedirect('/')


class Search(View):
    def find_products(self, arg):
        result = []
        content_models = ContentType.objects.filter(model__in=['mod', 'mechmod'])
        for model in content_models:
            result.extend(model.model_class().objects.filter(title__istartswith=arg))
        print(result)
        return result

    def get(self, request, *args, **kwargs):
        search_arg = request.GET['searchbox']
        products = self.find_products(search_arg)
        return render(request, 'search.html', {'products': products})
