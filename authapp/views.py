from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, UserProfileEditForm
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    title = 'GeekShop - Регистрация'
    success_url = reverse_lazy('auth:login')

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            # ToDo Ok_kir - необходимо проверить необходимость данной передачи сообщений (возможно упрощение)
            list(messages.get_messages(request))  # Очищаем сообщения (т.к. они реализованы генератором)
            if self.send_verify_mail(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Сообщение для подтверждения отправлено.')
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Ошибка отправки сообщения')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def send_verify_mail(user):
        verify_link = reverse('authapp:verify', kwargs={'email': user.email, 'activation_key': user.activation_key})
        subject = f'Account Verifications {user.username}'
        message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} ' \
                  f'перейдите по ссылке \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(self, 'authapp/verification.html')
        except Exception as err:
            print(f'Error activation user : {err.args}')
            return HttpResponseRedirect(reverse('mainapp:index'))


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    template_name = 'authapp/profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('authapp:profile')
    title = 'GeekShop - Профиль'

    def post(self, request, *args, **kwargs):
        form = UserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            messages.set_level(self.request, messages.INFO)
            messages.info(self.request, "Информация о пользователе изменена.")
            form.save()
            # profile_form.save()
        return redirect(self.success_url)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile_form'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context


class Logout(LogoutView):
    # Путь после logout указан в LOGOUT_REDIRECT_URL (settings.py)
    pass
