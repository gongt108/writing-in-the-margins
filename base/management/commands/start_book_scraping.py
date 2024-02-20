# myapp/management/commands/start_scraping.py

from django.core.management.base import BaseCommand
from base.views import start_book_scraping


class Command(BaseCommand):
    help = "Starts the Scrapy crawler process"

    def add_arguments(self, parser):
        # Add an argument for the search query
        parser.add_argument("book_id", nargs="?", type=str, help="Book id")

    def handle(self, *args, **kwargs):
        # Get the search query argument
        book_id = kwargs["book_id"]
        start_book_scraping(book_id)
