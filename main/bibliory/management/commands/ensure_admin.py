import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.password_validation import validate_password


class Command(BaseCommand):
    help = 'Create or refresh the site administrator from environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '')
        email = os.environ.get('ADMIN_EMAIL', '').strip()

        if not username or not password:
            self.stdout.write('Admin bootstrap skipped: set ADMIN_USERNAME and ADMIN_PASSWORD.')
            return

        User = get_user_model()
        user, _created = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            raise CommandError(f'ADMIN_PASSWORD does not pass Django validation: {exc}') from exc
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Administrator "{username}" is ready.'))
