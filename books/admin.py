from django.contrib import admin

from books.models import Person, Language, Book

# Register your models here.
admin.site.register(Person)
admin.site.register(Language)
admin.site.register(Book)
