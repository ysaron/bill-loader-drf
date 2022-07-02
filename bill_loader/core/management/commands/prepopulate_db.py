from django.core.management.base import BaseCommand

from core.models import Service
from core.services.classifier import services


class Command(BaseCommand):
    help = 'Заполняет БД данными о доступных сервисах'

    def handle(self, *args, **options):
        self.stdout.write('Writing services...')
        for cls, name in services.items():
            Service.objects.get_or_create(cls=cls, name=name)
        self.stdout.write('Done')
