from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        print(timezone.localtime())