from django.db import models

from besth_backend.common import AbstractBaseModel


class OilBase(AbstractBaseModel):
    """Модель нефтебазы"""

    ksss_code = models.IntegerField(unique=True, verbose_name="Код КССС НБ")
    name = models.CharField(max_length=255, verbose_name="Название нефтебазы")
    region = models.CharField(max_length=255, verbose_name="Регион нефтебазы")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес нефтебазы")

    def __str__(self):
        return f"{self.name} (Код: {self.ksss_code})"

    class Meta:
        verbose_name = "Нефтебаза"
        verbose_name_plural = "Нефтебазы"
