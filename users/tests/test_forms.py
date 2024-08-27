from django.test import TestCase
from users.forms import RegisterForm
from users.models import User


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form = RegisterForm(data={
            'email': 'newuser@test.com',
            'password1': 'testpassword1234',
            'password2': 'testpassword1234',
            'birthday': '2001-01-01',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890'
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, 'newuser@test.com')

    def test_invalid_form(self):
        form = RegisterForm(data={
            'email': 'newuser@test12.com',
            'password1': 'testpassword',
            'password2': 'testpassword123456',
            'birthday': '2001-01-01',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890'
        })
        self.assertFalse(form.is_valid(), form.errors)
        self.assertEqual(User.objects.count(), 0)
