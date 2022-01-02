import os

import requests
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from authapp.models import UserProfile
from geekshop.settings import MEDIA_ROOT


def _save_user_vk(user, response, *args, **kwargs):
    # Запрос условно скрытой информации
    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(OrderedDict(
                              fields=','.join(('bdate', 'sex', 'about', 'photo_200', 'personal')),
                              access_token=response['access_token'], v=5.131)), None))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    # ----------------------------------------
    data = resp.json()['response'][0]
    if data['sex'] == 1:
        user.userprofile.sex = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.sex = UserProfile.MALE
    else:
        pass
    # ----------------------------------------
    if data['about']:
        user.userprofile.about = data['about']
    # ----------------------------------------
    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        user.age = age
        if age < 10:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    # ----------------------------------------
    if data['photo_200']:
        response_url_image = requests.get(data['photo_200'])
        if response_url_image.status_code == 200:
            file_name = f'avatar_{user.username}.jpg'
            with open(f'{MEDIA_ROOT}{os.sep}{file_name}', 'wb') as f:
                f.write(response_url_image.content)
            user.image = file_name
    # ----------------------------------------
    if data['personal'].get('langs'):
        user.userprofile.langs = ', '.join(data['personal'].get('langs'))
    user.save()


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        _save_user_vk(user, response, *args, **kwargs)
