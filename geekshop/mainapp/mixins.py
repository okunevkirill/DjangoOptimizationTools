import re

from django import forms
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.views.generic.base import ContextMixin


class TitleContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


# -------------------------------------------------------------------------------
class AdminAccessOnlyMixin(UserPassesTestMixin):
    """Verification conditions for the administrator"""

    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.is_superuser


class StaffAccessOnlyMixin(UserPassesTestMixin):
    """Verification conditions for the staff"""

    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


# -------------------------------------------------------------------------------
class CssFormMixin:
    SPECIAL_FIELDS = {
        'category': 'form-control',
        'image': 'custom-file-input',
        'sex': 'form-control',
    }

    def set_field_styles(self, fields: dict) -> None:
        """Функция установка стилей css для методов __init__ в классах форм"""
        for field_name, field in fields.items():
            style_css = self.SPECIAL_FIELDS.get(field_name, 'form-control py-4')
            field.widget.attrs['class'] = style_css


# -------------------------------------------------------------------------------
class ValidatorUserFormMixin(forms.ModelForm):
    def clean_username(self):
        data = self.cleaned_data['username']
        if not data:
            raise forms.ValidationError("Никнеймом - обязательное поле")
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{3,}$', data):
            raise forms.ValidationError(
                'Никнейм должен начинаться с буквы, состоять из латинских букв или цифр и быть длиной от 4 символов')
        return data


# -------------------------------------------------------------------------------
class SpecializedRemovalDeleteViewMixin(DeleteView):
    def __init__(self, *args, **kwargs):
        self.object = None  # [*] Необязательное действие - для избегания варнинга в IDE
        super().__init__(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# -------------------------------------------------------------------------------
class ProductQuantityMixin:
    objects = None

    def get_product_quantity(self, pk):
        return self.__class__.objects.get(pk=pk).quantity