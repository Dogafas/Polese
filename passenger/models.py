from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import re


def validate_passport_series(value):
    """Проверка корректности серии паспорта."""
    if value and not re.fullmatch(
        r"\d{4}", value
    ):  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: (Проверка на пустое значение)
        raise ValidationError(
            "Некорректный формат серии паспорта. Ожидаемый формат: 'XXXX'"
        )


def validate_passport_number(value):
    """Проверка корректности номера паспорта."""
    if value and not re.fullmatch(
        r"\d{6}", value
    ):  # <-ЗДЕСЬ ИЗМЕНЕНИЯ: (Проверка на пустое значение)
        raise ValidationError(
            "Некорректный формат номера паспорта. Ожидаемый формат: 'XXXXXX'"
        )


class Passenger(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь"
    )
    first_name = models.CharField(max_length=50, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=False, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=False, verbose_name="Отчество")
    phone_number = PhoneNumberField(
        blank=False, region="RU", verbose_name="Номер телефона"
    )
    passport_series = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name="Серия паспорта",
        validators=[validate_passport_series],
    )
    passport_number = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name="Номер паспорта",
        validators=[validate_passport_number],
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Пассажир"
        verbose_name_plural = "Пассажиры"
