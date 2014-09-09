from django.core.management.base import BaseCommand
from main.models import Data
from datetime import datetime, timedelta

class Command(BaseCommand):
    
    def clean_up_data(self):
        time_threshold = datetime.now() - timedelta(days=14)
        to_delete = Data.objects.filter(timestamp__lt=time_threshold)
        for instance in to_delete:
            instance.delete()
        print("Huhu")
