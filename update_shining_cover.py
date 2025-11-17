import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Update The Shining book with cover image
try:
    book = Book.objects.get(title="The Shining", author="Stephen King")
    book.cover_image = "https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1353277730i/11588.jpg"
    book.save()
    print(f"✓ Successfully updated cover image for '{book.title}' by {book.author}")
except Book.DoesNotExist:
    print("✗ The Shining by Stephen King not found in database")
except Exception as e:
    print(f"✗ Error: {e}")
