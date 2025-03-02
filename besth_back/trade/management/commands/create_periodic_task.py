from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = 'Create a periodic task'

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=12,
            period=IntervalSchedule.HOURS,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name='Cleaning lot task',
            task='lot_cleaning',
        )

        self.stdout.write(self.style.SUCCESS('Periodic task created.'))
