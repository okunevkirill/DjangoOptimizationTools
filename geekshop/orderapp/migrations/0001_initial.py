# Generated by Django 3.2.8 on 2022-01-26 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mainapp.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='СОЗДАН')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='ОБНОВЛЁН')),
                ('status', models.CharField(choices=[('F', 'ФОРМИРУЕТСЯ'), ('S', 'ОТПРАВЛЕН В ОТРАБОТКУ'), ('P', 'ОПЛАЧЕН'), ('W', 'ОБРАБАТЫВАЕТСЯ'), ('R', 'ГОТОВ К ВЫДАЧЕ'), ('C', 'ОТМЕНЕН')], default='F', max_length=1, verbose_name='СТАТУС')),
                ('is_active', models.BooleanField(default=True, verbose_name='АКТИВНЫЙ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ЗАКАЗ',
                'verbose_name_plural': 'ЗАКАЗЫ',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=0, verbose_name='КОЛИЧЕСТВО')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='orderapp.order', verbose_name='ЗАКАЗ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='ПРОДУКТЫ')),
            ],
            bases=(mainapp.mixins.ProductQuantityMixin, models.Model),
        ),
    ]
