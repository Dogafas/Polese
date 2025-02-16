from django.db import models


class Ship(models.Model):
    ship_id = models.AutoField(primary_key=True, verbose_name="ID судна")
    name = models.CharField(max_length=255, unique=True, verbose_name="Название судна")
    capacity = models.IntegerField(verbose_name="Вместимость, пасс.")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Судно"
        verbose_name_plural = "Судно/теплоход"
