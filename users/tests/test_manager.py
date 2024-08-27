from django.test import TestCase
from users.models import User


class UserManagerTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='user@test.com',
            password='pass',
            birthday='2000-01-01'
        )
        self.assertEqual(user.email, 'user@test.com')
        self.assertTrue(user.check_password('pass'))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='pass',
            birthday='1990-01-01'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
