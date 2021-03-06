# Generated by Django 3.1.5 on 2021-02-08 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0008_auto_20210206_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False, verbose_name='В заказе'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_name', models.CharField(max_length=255, verbose_name='ФИО покупателя')),
                ('buyer_phone_number', models.CharField(max_length=25, verbose_name='Номер телефона')),
                ('buyer_address', models.CharField(max_length=400, verbose_name='Адрес')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Стоимость')),
                ('order_time', models.DateTimeField(auto_now=True, verbose_name='Время заказа')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.cart', verbose_name='Корзина')),
            ],
        ),
    ]
