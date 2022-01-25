from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    FEMALE = 'W'
    MALE = 'M'
    GENDER_CHOICES = (
        ('', 'НЕ УКАЗАН'),
        (FEMALE, 'ЖЕНСКИЙ'),
        (MALE, 'МУЖСКОЙ'),
    )
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users_image', blank=True, verbose_name='ИЗОБРАЖЕНИЕ')
    age = models.PositiveSmallIntegerField(null=True, verbose_name='ВОЗРАСТ')
    about = models.TextField(blank=True, null=True, max_length=512, verbose_name='О СЕБЕ')
    sex = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=1, verbose_name='ПОЛ')
    activation_key = models.CharField(max_length=128, blank=True, verbose_name='КЛЮЧ ПОДТВЕРЖДЕНИЯ')
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, verbose_name='СРОК КЛЮЧА')

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires + timedelta(hours=24):
            return False
        return True
