from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Person, Book


class AuthorsViewTests(APITestCase):
    # @TODO: Add simpler tests for each subcase (n/a dates, ordered by download counts, etc...)

    def setUp(self):
        # Create Authors
        author1 = Person.objects.create(name="Victor Michel", birth_year=1797, death_year=1877)
        author2 = Person.objects.create(name="Jean de Rose", death_year=1304)
        author3 = Person.objects.create(name="Guillaume")

        # Create Books
        book1 = Book.objects.create(title="Book 1", media_type="text", copyright=False, download_count=100,
                                    subjects_json={}, bookshelves_json={}, formats_json={})
        book1.authors.set([author1, author2])

        book2 = Book.objects.create(title="Book 2", media_type="text", copyright=True, download_count=200,
                                    subjects_json={}, bookshelves_json={}, formats_json={})
        book2.authors.set([author1])

        book3 = Book.objects.create(title="Book 3", media_type="text", copyright=False, download_count=50,
                                    subjects_json={}, bookshelves_json={}, formats_json={})
        book3.authors.set([author3])

    def test_authors_list(self):
        """Test that the authors list is returned correctly."""
        url = reverse('authors')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_results = [
            {
                "name": "Victor Michel",
                "date": "1797 - 1877",
                "number_of_books": 2,
                "number_of_bookshelves": 0,
                "total_download_count": 300
            },
            {
                "name": "Jean de Rose",
                "date": "n/a - 1304",
                "number_of_books": 1,
                "number_of_bookshelves": 0,
                "total_download_count": 100
            },
            {
                "name": "Guillaume",
                "date": "n/a",
                "number_of_books": 1,
                "number_of_bookshelves": 0,
                "total_download_count": 50
            }
        ]

        self.assertEqual(response.data['results'], expected_results)
