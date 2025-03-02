from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

from trade.models import FuelType, OilBase

from besth_backend.common import AbstractBaseModel


class Lot(AbstractBaseModel):
    """Модель лота топлива"""

    STATUS_CHOICES = (
        ('confirmed', 'Подтвержден'),
        ('sold', 'Продан'),
        ('inactive', 'Неактивен'),
    )
    expiration_date = models.DateField(verbose_name="Дата лота")
    oil_base = models.ForeignKey(
        OilBase,
        on_delete=models.CASCADE,
        related_name='lots',
        verbose_name="Нефтебаза"
    )
    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.CASCADE,
        related_name='lots',
        verbose_name="Вид топлива"
    )
    initial_volume = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000000'))],
        verbose_name="Стартовый вес (т)",
    )
    available_volume = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000000'))],
        verbose_name="Доступный остаток (т)"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='confirmed',
        verbose_name="Статус"
    )
    price_per_ton = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Цена за 1 тонну (руб)"
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_volume = self.initial_volume

        if self.pk:
            if self.available_volume <= 0:
                self.status = 'sold'
            elif self.expiration_date < timezone.now().date():
                self.status = 'inactive'

        super().save(*args, **kwargs)
    
    @property
    def total_price(self):
        return self.price_per_ton * self.available_volume

    def __str__(self):
        return f"Лот #{self.pk} - {self.fuel_type.name} на {self.oil_base.name} - {self.expiration_date}"

    class Meta:
        verbose_name = "Лот"
        verbose_name_plural = "Лоты"
        ordering = ['-expiration_date', 'id']
