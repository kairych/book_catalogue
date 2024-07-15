from django.contrib.auth import get_user_model
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Description')
    publication_date = models.DateField(verbose_name='Publication Date')
    genre = models.ManyToManyField(
        'books.Genre',
        related_name='books',
        verbose_name='Genre'
    )
    author = models.ManyToManyField(
        'books.Author',
        related_name='books',
        verbose_name='Author'
    )
    favorites = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='favorite_books',
        verbose_name='Favorites'
    )

    def __str__(self):
        author_names = ", ".join(author.name for author in self.author.all())
        return f'{self.title} by {author_names}'


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name='Author name')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Genre')

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(max_length=3000, verbose_name='Review')
    rating = models.IntegerField(
        null=True,
        blank=True,
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        verbose_name='Rating'
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Book'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return f'{self.text:30} by {self.author}'
