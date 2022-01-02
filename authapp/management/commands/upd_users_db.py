from django.core.management.base import BaseCommand
from authapp.models import User, UserProfile


class Command(BaseCommand):
    help = 'Adds userprofile to already created users'

    def handle(self, *args, **options):
        users_to_update = User.objects.filter(userprofile__isnull=True)
        print(f'Found {users_to_update.count()} users')
        for user in users_to_update:
            UserProfile.objects.create(user=user)
        print('[*] - End script')
