# Generated by Django 3.2.8 on 2022-01-02 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0005_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',), 'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
    ]
