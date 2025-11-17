import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Update Azul Board Game with cover image
try:
    book = Book.objects.get(title="Azul Board Game")
    book.cover_image = "https://m.media-amazon.com/images/I/81SwhgYw8UL.jpg"
    book.save()
    print(f"✓ Successfully updated cover image for '{book.title}' by {book.author}")
except Book.DoesNotExist:
    print("✗ Azul Board Game not found in database")
except Exception as e:
    print(f"✗ Error: {e}")
