from celery import shared_task
import logging 
from django.utils import timezone
from trade.models import Lot


logger = logging.getLogger('common')


@shared_task(name="lot_cleaning")
def clean_excited_lots():
    logger.info('Cleaning excited lots started.')
    Lot.objects.filter(expiration_date__lt=timezone.now().date()).update(status='inactive')
    logger.info('Cleaning excited lots finished.')
