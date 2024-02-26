# myapp/management/commands/start_scraping.py

from django.core.management.base import BaseCommand
from base.views import daily_price_scraping


class Command(BaseCommand):
    help = "Starts the Scrapy crawler process"

    def handle(self, *args, **kwargs):

        daily_price_scraping()
