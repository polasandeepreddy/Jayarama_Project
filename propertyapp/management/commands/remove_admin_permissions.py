from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Remove admin privileges from a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully removed admin privileges from {username}.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist.'))
