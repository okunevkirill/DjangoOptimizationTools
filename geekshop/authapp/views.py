from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, UpdateView
from django.contrib import messages, auth

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User
from mainapp.mixins import TitleContextMixin


class UserLogin(TitleContextMixin, LoginView):
    """Контроллер аутентификации пользователя"""
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True
    form_class = UserLoginForm
    title = 'GeekShop | Авторизация'


class UserRegister(TitleContextMixin, FormView):
    """Контроллер регистрации нового пользователя"""
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    title = 'GeekShop | Регистрация'
    success_url = reverse_lazy('auth:login')

    def dispatch(self, request, *args, **kwargs):   # ToDo - Модернизировать защиту
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mainapp:index'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            # ToDo Ok_kir - необходимо проверить необходимость данной передачи сообщений (возможно упрощение)
            list(messages.get_messages(request))  # Очищаем сообщения (т.к. они реализованы генератором)
            if self._send_verify_mail(user):
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
    def _send_verify_mail(user):
        verify_link = reverse(
            'authapp:verification',
            kwargs={'email': user.email, 'activation_key': user.activation_key}
        )
        subject = f'Account Verifications {user.username}'
        message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} ' \
                  f'перейдите по ссылке \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)


class UserLogout(LogoutView):
    """Контроллер выхода из-под пользователя"""
    pass  # Путь после logout указан в LOGOUT_REDIRECT_URL (settings.py)


def user_verification(request, email, activation_key):
    """Контроллер подтверждения регистрации"""
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html',
                          context={'title': 'GeekShop | Активация профиля'})
    except Exception as err:
        print(f'Error activation user : {err.args}')
    return HttpResponseRedirect(reverse('mainapp:index'))


class UserInfo(TitleContextMixin, LoginRequiredMixin, UpdateView):
    """Контроллер с информацией о пользователе"""

    template_name = 'mainapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    title = 'GeekShop | Профиль'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            messages.set_level(self.request, messages.INFO)
            messages.info(self.request, "Информация о пользователе изменена.")
            form.save()
        return redirect(self.success_url)

    def get_object(self, *args, **kwargs):
        return self.request.user  # [*] Переопределил для скрытия id пользователя

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['baskets'] = self.request.user.basket.all()
        return context
