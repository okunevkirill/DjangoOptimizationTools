from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from mainapp.mixins import CssFormMixin, ValidatorUserFormMixin
from mainapp.models import ProductCategory, Product


class UserAdminappCreationForm(ValidatorUserFormMixin, CssFormMixin, UserCreationForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    age = forms.IntegerField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'age',
                  'password1', 'password2', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_field_styles(self.fields)


class UserAdminappChangeForm(ValidatorUserFormMixin, CssFormMixin, UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'image', 'age')

    age = forms.IntegerField()
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    email = forms.EmailField(widget=forms.EmailInput())
    username = forms.CharField(widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = False
        self.fields['username'].widget.attrs['readonly'] = False
        self.set_field_styles(self.fields)


# -------------------------------------------------------------------------------
class CategoryAdminappForm(CssFormMixin, forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_field_styles(self.fields)


# -------------------------------------------------------------------------------
class ProductAdminappForm(CssFormMixin, forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all())
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_field_styles(self.fields)
