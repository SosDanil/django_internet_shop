from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='sos.danil@yandex.ru',
            first_name='Danil',
            last_name='Klimenko',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('225335445s')
        user.save()
