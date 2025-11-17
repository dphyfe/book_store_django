import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Update Atomic Habits book with cover image
try:
    book = Book.objects.get(title="Atomic Habits", author="James Clear")
    book.cover_image = "https://m.media-amazon.com/images/I/81kg51XRc1L._AC_UF1000,1000_QL80_.jpg"
    book.save()
    print(f"✓ Successfully updated cover image for '{book.title}' by {book.author}")
except Book.DoesNotExist:
    print("✗ Atomic Habits by James Clear not found in database")
except Exception as e:
    print(f"✗ Error: {e}")
