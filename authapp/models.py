from datetime import timedelta

import pytz
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True)
    email = models.EmailField(unique=True, blank=False)
    age = models.PositiveSmallIntegerField(
        default=18,
        validators=[MinValueValidator(1), MaxValueValidator(150)],
        verbose_name='Возраст',
    )
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True)

    def is_activation_key_expired(self):
        """Checking the validity of the user's activation key"""
        # if now() > self.activation_key_expires + timedelta(hours=24):
        if self.activation_key_expires < (now() - timedelta(hours=24)).replace(tzinfo=pytz.UTC):
            return True
        return False
