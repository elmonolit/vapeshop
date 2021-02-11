from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_save

from pytils.translit import slugify


class ProductsForMainPage:
    def get_products(*args):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct in ct_models:
            model_products = ct.model_class()._base_manager.all()
            # model_products = ct.model_class().objects.all()
            products.extend(model_products)
        return products


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.category_name

    def save(self):
        self.slug = slugify(self)
        super(Category, self).save()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name='Название мода')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    diameter = models.CharField(verbose_name='Диаметр посадки атомайзера', max_length=50)
    connector = models.CharField(verbose_name='Тип коннектора', max_length=255)
    amount_of_acb = models.PositiveSmallIntegerField(verbose_name='Количество аккумуляторов', default=1)

    slug = models.SlugField(unique=True, blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self)
        super().save(*args,**kwargs)

    def get_model_name(self):
        return self._meta.model_name

    def get_absolute_url(self):
        ct_model = self.get_model_name()
        return reverse('product_detail', kwargs={'ct_model': ct_model, 'slug': self.slug})



    def __str__(self):
        return self.title


class Mod(Product):
    power = models.PositiveIntegerField(verbose_name='Мощность')
    accum = models.BooleanField(verbose_name='Налисие аккумулятора')
    accum_capacity = models.PositiveIntegerField('Емкость аккумулятора', blank=True, null=True)
    accum_type = models.CharField(verbose_name='Тип аккумулятора', max_length=255, blank=True, null=True)
    thermal_control = models.BooleanField(verbose_name='Термоконтроль', default=False)
    image = models.ImageField(upload_to='mod')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Эдектронный мод'
        verbose_name_plural = 'Электронные моды'


class MechMod(Product):
    material = models.CharField(verbose_name='Материал', max_length=255)
    accum_type = models.CharField(verbose_name='Тип аккумулятора', max_length=255)
    image = models.ImageField(upload_to='mechmod')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Механический мод'
        verbose_name_plural = 'Механические моды'


class CartProduct(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(verbose_name='Количество', default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, verbose_name='Обзая цена')

    def __str__(self):
        return "Продукт: {} для корзины".format(self.content_object.title)

    def save(self,*args,**kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args,**kwargs)

    class Meta:
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'


class Cart(models.Model):
    owner = models.ForeignKey(User, verbose_name='Владелец корзины', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, verbose_name='Продукты', blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Кол-во продуктов')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Общая цена корзины')

    def __str__(self):
        return str(self.id) + "корзина"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # self.final_price = sum([fp.final_price for fp in self.products.all()])
