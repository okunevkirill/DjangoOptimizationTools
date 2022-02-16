from django.test import TestCase
from django.test.client import Client
from django.utils.timezone import now
from datetime import timedelta

from authapp.models import User

_SUPERUSER = {'username': 'admin', 'first_name': 'admin', 'last_name': 'admin',
              'email': 'admin@gmail.com', 'password': 'tEsT1234', 'age': 34, 'sex': User.MALE}
_REGULAR_USER = {'username': 'user', 'first_name': 'user', 'last_name': 'user',
                 'email': 'user@gmail.com', 'password': 'tEsT1234cfg', 'age': 22, 'sex': User.FEMALE}
_NEW_USER = {'username': 'django1', 'first_name': 'django1', 'last_name': 'django1',
             'email': 'django1@mail.ru', 'password1': 'Geekshop1231_',
             'password2': 'Geekshop1231_', 'age': 31}


class TestUri(TestCase):
    superuser = _SUPERUSER.copy()
    regular_user = _REGULAR_USER.copy()
    new_user = _NEW_USER.copy()

    @classmethod
    def setUpClass(cls):
        User.objects.create_superuser(
            cls.superuser['username'], cls.superuser['email'], cls.superuser['password'])
        User.objects.create_user(
            cls.regular_user['username'], cls.regular_user['email'], cls.regular_user['password'])

    def setUp(self) -> None:
        self.client = Client()

    def test_login(self):
        # Тестирование незарегистрированного пользователя
        response = self.client.get(r'/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        response = self.client.get(r'/user/login/')
        self.assertEqual(response.status_code, 200)
        # -----------------------------------------------------
        self.client.login(
            username=self.superuser['username'], password=self.superuser['password'])
        response = self.client.get(r'/user/login/')
        self.assertEqual(response.status_code, 302)  # Переадресация после аутентификации

    def test_register(self):
        response = self.client.get(r'/user/register/')
        self.assertEqual(response.status_code, 200)
        # -----------------------------------------------------
        response = self.client.post(r'/user/register/', data=self.new_user)
        self.assertEqual(response.status_code, 302)  # Переадресация после регистрации
        user = User.objects.get(username=self.new_user['username'])
        self.assertFalse(user.is_active)  # Пользователь до подтверждения должен быть не активен
        activation_url = fr'/user/verification/{user.email}/{user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.client.logout()
        # -----------------------------------------------------
        self.client.login(
            username=self.regular_user['username'], password=self.regular_user['password'])
        response = self.client.get(r'/user/register/')
        self.assertEqual(response.status_code, 302)  # Переадресация авторизированного пользователя

    def test_profile(self):
        response = self.client.get(r'/user/profile/')
        self.assertEqual(response.url, '/user/login/?next=/user/profile/')
        self.assertEqual(response.status_code, 302)  # Переадресация НЕ авторизированного пользователя
        # -----------------------------------------------------
        self.client.login(
            username=self.regular_user['username'], password=self.regular_user['password'])
        response = self.client.get(r'/user/profile/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(r'/user/logout/')
        self.assertEqual(response.status_code, 302)  # Переадресация НЕ авторизированного пользователя
        # -----------------------------------------------------
        self.client.login(
            username=self.superuser['username'], password=self.superuser['password'])
        response = self.client.get(r'/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        self.client.get(r'/user/logout/')  # Выходим из-под пользователя
        response = self.client.get(r'/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    @classmethod
    def tearDownClass(cls):
        pass


class TestModels(TestCase):
    def setUp(self) -> None:
        self.regular_user = _REGULAR_USER.copy()
        self.user = User.objects.create(**self.regular_user)
        self.user.is_active = False

    def test_is_activation_key_expired(self):
        self.assertFalse(self.user.is_activation_key_expired())  # Время ссылки не истекло
        # -----------------------------------------------------
        self.user.activation_key_expires = now() - timedelta(hours=40)
        self.assertTrue(self.user.is_activation_key_expired())

    def tearDown(self) -> None:
        pass
