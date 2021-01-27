from django.db import models
from pytils.translit import slugify


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
    description = models.TextField(verbose_name='Описание', blank=True, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title


class Mod(Product):
    power = models.PositiveIntegerField(verbose_name='Мощность')
    accum = models.BooleanField(verbose_name='Налисие аккумулятора')
    accum_capacity = models.PositiveIntegerField('Емкость аккумулятора')
    accum_type = models.CharField(verbose_name='Тип аккумулятора', max_length=255)
    image = models.ImageField(upload_to='mod')

    def __str__(self):
        return self.title

    def save(self):
        self.slug = slugify(self)
        super(Mod, self).save()

    class Meta:
        verbose_name = 'Эдектронный мод'
        verbose_name_plural = 'Электронные моды'


class MechMod(Product):
    material = models.CharField(verbose_name='Материал', max_length=255)
    connector = models.CharField(verbose_name='Тип коннектора', max_length=255)
    accum_type = models.CharField(verbose_name='Тип аккумулятора', max_length=255)
    image = models.ImageField(upload_to='mechmod')

    def __str__(self):
        return self.title

    def save(self):
        self.slug = slugify(self)
        super(MechMod, self).save()

    class Meta:
        verbose_name = 'Механический мод'
        verbose_name_plural = 'Механические моды'
