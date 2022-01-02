from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.base import View, ContextMixin
from django import forms


class AdministratorAccessOnlyMixin(UserPassesTestMixin):
    """Verification conditions for the administrator"""

    def test_func(self):
        return self.request.user.is_superuser


class StaffAccessOnlyMixin(UserPassesTestMixin):
    """Verification conditions for the staff"""

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class BaseClassContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class UserDispatchMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDispatchMixin, self).dispatch(request, *args, **kwargs)


# -------------------------------------------------------------------------------
# Mixin for Form
class CssFormattingMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
