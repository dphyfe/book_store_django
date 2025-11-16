from django.db import models


class Book(models.Model):
    """Model representing a book in the bookstore."""

    CATEGORY_CHOICES = [
        ("fiction", "Fiction"),
        ("nonfiction", "Non-Fiction"),
        ("teens_kids", "Teens/Kids"),
        ("audiobook", "Audiobook"),
        ("toys_games", "Toys & Games"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    isbn = models.CharField(max_length=13, unique=True)
    cover_image = models.URLField(blank=True, null=True)
    publication_date = models.DateField()
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
