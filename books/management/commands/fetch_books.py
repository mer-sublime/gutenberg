from urllib.parse import urlencode

import requests
from django.core.management.base import BaseCommand

from books.models import Book, Person, Language


class Command(BaseCommand):
    help = 'Fetch books from Gutendex API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            help='Number of pages to fetch (each page contains 32 books)',
            default=1  # Default to fetching 1 page
        )

        parser.add_argument(
            '--start-page',
            type=int,
            help='Page number to start fetching from (starting at 1)',
            default=1  # Default to starting from page 1
        )

    @staticmethod
    def generate_url(page):
        """Generate the URL to fetch books from Gutendex based on the start page."""
        base_url = 'https://gutendex.com/books'
        params = {
            'languages': 'fr', # @TODO Could be another parameter for the custom command
            'page': page,
        }
        return f'{base_url}?{urlencode(params)}'


    def handle(self, *args, **kwargs):
        pages_to_fetch = kwargs['pages']
        start_page = kwargs['start_page']

        if pages_to_fetch < 1 or start_page < 1:
            self.stdout.write(self.style.ERROR('Pages and start-page must be positive integers.'))
            return

        # Print usage string
        self.stdout.write(self.style.NOTICE(f'Fetching {pages_to_fetch} page(s) starting from page {start_page}...'))

        url = self.generate_url(page=start_page)
        while pages_to_fetch > 0:

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f'Failed to parse JSON response: {e}'))
                break
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Failed to fetch books from Gutendex: {e}'))
                break

            for item in data['results']:
                # Get or create Authors
                authors = []
                for author_data in item['authors']:
                    author, _ = Person.objects.get_or_create(
                        name=author_data['name'],
                        defaults={
                            'birth_year': author_data.get('birth_year'),
                            'death_year': author_data.get('death_year')
                        }
                    )
                    authors.append(author)

                # Get or create Languages
                languages = [Language.objects.get_or_create(code=code)[0] for code in item['languages']]

                # Get or create Book
                book, created = Book.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'title': item['title'],
                        'media_type': item['media_type'],
                        'copyright': item['copyright'],
                        'download_count': item['download_count'],
                        'subjects_json': item['subjects'],
                        'bookshelves_json': item['bookshelves'],
                        'formats_json': item['formats'],
                    }
                )
                # Set many-to-many relationships
                book.authors.set(authors)
                book.languages.set(languages)
                book.save() # @TODO: A bulk_create() would be more efficient at some point.

            # One page less to fetch
            pages_to_fetch -= 1

            # Update the URL for the next iteration
            url = data.get('next')
            if not url:
                break

        # @TODO: Condition and modify the success message to show how many new books were stored.
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored books.'))
