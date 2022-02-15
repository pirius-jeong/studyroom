from django.core.management.base import BaseCommand
from studyroom.com import bill_dml

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):

        bill_dml()
