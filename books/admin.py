from django.contrib import admin
from .models import Book, Author, Genre, Review


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publication_date', 'display_authors', 'display_genres', )
    list_filter = ('publication_date', 'genre', 'author')
    search_fields = ('title', 'author__name', 'genre__name')
    ordering = ('title', )
    date_hierarchy = 'publication_date'

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.author.all()])
    display_authors.short_description = 'Authors'

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    display_genres.short_description = 'Genres'


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Review)
