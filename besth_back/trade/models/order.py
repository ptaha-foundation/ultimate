from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

from trade.models import Lot, OilBase, FuelType

from besth_backend.common import AbstractBaseModel


class Order(AbstractBaseModel):
    """Модель заказа на покупку топлива"""

    DELIVERY_CHOICES = (
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка'),
    )

    lot = models.ForeignKey(
        Lot,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Лот"
    )
    oil_base = models.ForeignKey(
        OilBase,
        on_delete=models.CASCADE,
        related_name='orders_oil_base',
        verbose_name='Нефтяная база'
    )
    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.CASCADE,
        related_name='orders_fuel_type',
        verbose_name='Вид топлива'
    )
    volume = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000000'))],
        verbose_name="Объём заказа (л)"
    )
    delivery_type = models.CharField(
        max_length=10,
        choices=DELIVERY_CHOICES,
        default='pickup',
        verbose_name="Тип доставки"
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_user',
        verbose_name="Клиент"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Стоимость сделки за у.е. (руб)"
    )
    delivery_address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Адрес доставки"
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.oil_base_code = self.lot.oil_base.ksss_code
            self.fuel_type_code = self.lot.fuel_type.ksss_code

            self.price = (self.volume * self.lot.price_per_ton)

            lot = self.lot
            if lot.status != 'confirmed':
                return False
            lot.available_volume -= self.volume
            lot.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ #{self.id} от {self.created.strftime('%d.%m.%Y')}"
    
    @property
    def total_price(self):
        return self.price * self.volume

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created']
