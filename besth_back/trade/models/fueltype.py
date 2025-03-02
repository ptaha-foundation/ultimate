from django.db import models

from besth_backend.common import AbstractBaseModel


class FuelType(AbstractBaseModel):
    """Модель вида топлива"""

    ksss_code = models.IntegerField(unique=True, verbose_name="Код КССС Топлива")
    name = models.CharField(max_length=100, verbose_name="Наименование топлива")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name} (Код: {self.ksss_code})"

    class Meta:
        verbose_name = "Вид топлива"
        verbose_name_plural = "Виды топлива"
