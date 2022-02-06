import random
import hashlib
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms

from authapp.models import User
from mainapp.mixins import CssFormMixin, ValidatorUserFormMixin


class UserLoginForm(CssFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        self.set_field_styles(self.fields)


class UserRegisterForm(ValidatorUserFormMixin, CssFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите никнейм пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл.почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите  имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите  фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.set_field_styles(self.fields)

    def save(self, commit=True):
        user = super().save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class UserProfileForm(CssFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image', 'age', 'sex', 'about')

    image = forms.ImageField(widget=forms.FileInput(), required=False)
    age = forms.IntegerField(widget=forms.NumberInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.set_field_styles(self.fields)
