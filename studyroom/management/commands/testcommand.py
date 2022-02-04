from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        print("테스트 배치 프로그램 실행")