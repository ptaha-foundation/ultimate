from django.db import models
from django.utils import timezone


class AbstractBaseModel(models.Model):
    created = models.DateTimeField(
        default=timezone.now,
        editable=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True
