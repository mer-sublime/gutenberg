from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.code


class Bookshelf(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(blank=True, max_length=1024, null=True)
    authors = models.ManyToManyField(Person)
    translators = models.ManyToManyField(Person, related_name='books_translated')
    languages = models.ManyToManyField(Language)
    media_type = models.CharField(max_length=16)
    copyright = models.BooleanField(null=True)
    download_count = models.IntegerField()
    bookshelves = models.ManyToManyField(Bookshelf, related_name='books', blank=True)
    subjects_json = models.JSONField(null=True)
    formats_json = models.JSONField(null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)
