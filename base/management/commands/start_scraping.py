# myapp/management/commands/start_scraping.py

from django.core.management.base import BaseCommand
from base.views import start_scraping


class Command(BaseCommand):
    help = "Starts the Scrapy crawler process"

    def add_arguments(self, parser):
        # Add an argument for the search query
        parser.add_argument("search_query", nargs="?", type=str, help="Search query")

    def handle(self, *args, **kwargs):
        # Get the search query argument
        search_query = kwargs["search_query"]
        start_scraping(search_query)
