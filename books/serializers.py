from rest_framework import serializers

from .models import Person


class AuthorSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    number_of_books = serializers.IntegerField()
    number_of_bookshelves = serializers.IntegerField()
    total_download_count = serializers.IntegerField()

    class Meta:
        model = Person
        fields = ['name', 'date', 'number_of_books', 'number_of_bookshelves', 'total_download_count']

    def get_date(self, obj):
        birth_year = obj.birth_year if obj.birth_year else 'n/a'
        death_year = obj.death_year if obj.death_year else 'n/a'
        return f'{birth_year} - {death_year}'
