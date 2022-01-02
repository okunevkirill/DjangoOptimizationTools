from datetime import timedelta

import pytz
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        if self.activation_key_expires < (now() - timedelta(hours=24)).replace(tzinfo=pytz.UTC):
            return True
        return False


class UserProfile(models.Model):
    """Class-superstructure over User"""
    FEMALE = 'W'
    MALE = 'M'
    GENDER_CHOICES = (
        (FEMALE, 'женский'),
        (MALE, 'мужской'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    about = models.TextField(verbose_name='о себе', blank=True, null=True, max_length=512)
    sex = models.CharField(verbose_name='пол', choices=GENDER_CHOICES, blank=True, max_length=1)
    langs = models.CharField(verbose_name='знание языков', max_length=255, blank=True)

    @staticmethod
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        else:
            instance.userprofile.save()
