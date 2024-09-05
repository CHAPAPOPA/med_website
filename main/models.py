from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Speciality(models.Model):
    title = models.CharField(max_length=100, verbose_name="Наименование")
    icon = models.ImageField(upload_to="icons/", verbose_name="Иконка", **NULLABLE)
    description = models.TextField(verbose_name="описание", **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "специализация"
        verbose_name_plural = "специализации"


class Doctor(models.Model):

    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    photo = models.ImageField(upload_to="person/", verbose_name="Фото", **NULLABLE)
    speciality = models.ManyToManyField(
        "Speciality", verbose_name="Специализация", related_name="speciality"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "врач"
        verbose_name_plural = "врачи"


class Diagnostic(models.Model):
    title = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    price = models.PositiveIntegerField(verbose_name="стоимость")
    doctor = models.ManyToManyField("Doctor", related_name="врач")
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        verbose_name="специализация",
        related_name="услуги",
    )

    def __str__(self):
        return f"{self.title}: {self.price}"

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"


class Appointment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="записи",
        verbose_name="пациент",
        **NULLABLE,
    )
    diagnostic = models.ForeignKey(
        Diagnostic,
        on_delete=models.CASCADE,
        related_name="записи",
        verbose_name="диагностика",
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="записи", verbose_name="врач"
    )
    date = models.DateTimeField(verbose_name="дата и время приема")

    def __str__(self):
        return f"{self.user}: {self.date} {self.diagnostic}, {self.doctor}"

    class Meta:
        verbose_name = "запись на диагностику"
        verbose_name_plural = "записи на диагностику"

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        now = timezone.now()
        if self.date < now:
            raise ValidationError("Не допускается создавать записи в прошедшем времени")


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="имя")
    email = models.EmailField(unique=False, verbose_name="e-mail")
    text = models.TextField(verbose_name="текст")
    date = models.DateTimeField(verbose_name="дата и время отзыва")

    @classmethod
    def create(cls, name, email, text, date):
        feedback = cls(name=name, email=email, text=text, date=date)
        return feedback

    def __str__(self):
        return f"{self.name}: {self.email}"

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
