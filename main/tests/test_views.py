from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Appointment, Diagnostic, Doctor, Speciality
from users.models import User


class SpecialityListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Speciality.objects.create(title="Кардиология")
        Speciality.objects.create(title="Неврология")

    def test_view_url_exists_at_proper_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

    def test_lists_all_speciality(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["speciality_list"]) == 2)


class AppointmentListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@test.com", password="pass", birthday="2000-01-01"
        )
        self.client.login(email="user@test.com", password="pass")
        speciality = Speciality.objects.create(title="Кардиология")
        doctor = Doctor.objects.create(first_name="Иван", last_name="Иванов")
        diagnostic = Diagnostic.objects.create(
            title="ЭКГ", price=1000, speciality=speciality
        )
        diagnostic.doctor.add(doctor)
        Appointment.objects.create(
            user=self.user,
            diagnostic=diagnostic,
            doctor=doctor,
            date=timezone.now() + timezone.timedelta(days=1),
        )
        print(Appointment.objects.all())

    def test_view_url_exists_at_proper_location(self):
        response = self.client.get("/appointments/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("main:appointments"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/appointments.html")

    def test_lists_appointments(self):
        response = self.client.get(reverse("main:appointments"))
        print(response.context["appointment_list"])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["appointment_list"]) == 1)
