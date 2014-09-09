from django.core.management.base import BaseCommand
from main.models import Data
from datetime import datetime, timedelta

class Command(BaseCommand):
    
    help = 'Delete data instances older than 14 days'

    def add_argument(self):
        pass

    def handle(self, *args, **options):
        time_threshold = datetime.now() - timedelta(days=14)
        to_delete = Data.objects.filter(timestamp__lt=time_threshold)
        for instance in to_delete:
            instance.delete()
