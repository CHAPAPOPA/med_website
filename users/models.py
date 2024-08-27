from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=20, verbose_name="Фамилия")
    birthday = models.DateField(verbose_name="дата рождения")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telegram = models.CharField(
        unique=True, max_length=20, verbose_name="Telegram", **NULLABLE
    )
    phone = models.CharField(unique=True, max_length=20, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return (
            f'{self.first_name} {self.last_name} ({self.birthday.strftime("%d.%m.%Y")})'
        )

    class Meta:
        verbose_name = "пациент"
        verbose_name_plural = "пациенты"
