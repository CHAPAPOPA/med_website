from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@admin.com",
            telegram="admin",
            phone="88005553535",
            first_name="Админка",
            last_name="Админова",
            birthday="2000-01-01",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password("admin")
        user.save()
