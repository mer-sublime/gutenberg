from django.contrib import admin

from books.models import Person, Language, Book, Bookshelf

# Register your models here.
admin.site.register(Person)
admin.site.register(Language)
admin.site.register(Bookshelf)
admin.site.register(Book)
