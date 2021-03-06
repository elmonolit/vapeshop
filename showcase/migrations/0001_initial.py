# Generated by Django 3.1.5 on 2021-01-27 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, verbose_name='Название категории')),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название мода')),
                ('description', models.TextField(blank=True, unique=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('power', models.PositiveIntegerField(verbose_name='Мощность')),
                ('accum', models.BooleanField(verbose_name='Налисие аккумулятора')),
                ('accum_capacity', models.PositiveIntegerField(verbose_name='Емкость аккумулятора')),
                ('accum_type', models.CharField(max_length=255, verbose_name='Тип аккумулятора')),
                ('image', models.ImageField(upload_to='mod')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Эдектронный мод',
                'verbose_name_plural': 'Электронные моды',
            },
        ),
        migrations.CreateModel(
            name='MechMod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название мода')),
                ('description', models.TextField(blank=True, unique=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('material', models.CharField(max_length=255, verbose_name='Материал')),
                ('connector', models.CharField(max_length=255, verbose_name='Тип коннектора')),
                ('accum_type', models.CharField(max_length=255, verbose_name='Тип аккумулятора')),
                ('image', models.ImageField(upload_to='mechmod')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Механический мод',
                'verbose_name_plural': 'Механические моды',
            },
        ),
    ]
