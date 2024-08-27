from django.test import TestCase
from django.utils import timezone
from main.models import Speciality, Doctor, Diagnostic, Appointment, Feedback
from users.models import User
from django.core.exceptions import ValidationError


class SpecialityModelTest(TestCase):
    def test_string_representation(self):
        speciality = Speciality(title="Кардиология")
        self.assertEqual(str(speciality), speciality.title)

    def test_speciality_creation(self):
        speciality = Speciality.objects.create(
            title="Кардиология",
            description="Описание кардиологии"
        )
        self.assertEqual(speciality.title, "Кардиология")
        self.assertEqual(speciality.description, "Описание кардиологии")


class DoctorModelTest(TestCase):
    def test_string_representation(self):
        doctor = Doctor(first_name="Иван", last_name="Иванов")
        self.assertEqual(str(doctor), f"{doctor.first_name} {doctor.last_name}")

    def test_doctor_creation(self):
        speciality = Speciality.objects.create(title="Кардиология")
        doctor = Doctor.objects.create(
            first_name="Иван",
            last_name="Иванов",
        )
        doctor.speciality.add(speciality)
        self.assertIn(speciality, doctor.speciality.all())


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@example.com", birthday="2000-01-01")
        self.speciality = Speciality.objects.create(title="Кардиология")
        self.doctor = Doctor.objects.create(first_name="Иван", last_name="Иванов")
        self.diagnostic = Diagnostic.objects.create(
            title="ЭКГ",
            price=1000,
            speciality=self.speciality,
        )
        self.diagnostic.doctor.add(self.doctor)

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            user=self.user,
            diagnostic=self.diagnostic,
            doctor=self.doctor,
            date=timezone.now() + timezone.timedelta(days=1)
        )
        self.assertEqual(appointment.user, self.user)
        self.assertEqual(appointment.diagnostic, self.diagnostic)
        self.assertEqual(appointment.doctor, self.doctor)

    def test_past_appointment_validation(self):
        appointment = Appointment(
            user=self.user,
            diagnostic=self.diagnostic,
            doctor=self.doctor,
            date=timezone.now() - timezone.timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            appointment.clean_fields()


class FeedbackModelTest(TestCase):
    def test_feedback_creation(self):
        feedback = Feedback.objects.create(
            name="Тестовое имя",
            email="test@example.com",
            text="Тестовый отзыв",
            date=timezone.now()
        )
        self.assertEqual(feedback.name, "Тестовое имя")
        self.assertEqual(feedback.email, "test@example.com")
        self.assertEqual(feedback.text, "Тестовый отзыв")
