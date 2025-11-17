import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Update Circe book with cover image
try:
    book = Book.objects.get(title="Circe", author="Madeline Miller")
    # Using a direct image URL from Goodreads/Amazon
    book.cover_image = "https://m.media-amazon.com/images/I/81V7F8BUWPL._AC_UF1000,1000_QL80_.jpg"
    book.save()
    print(f"✓ Successfully updated cover image for '{book.title}' by {book.author}")
except Book.DoesNotExist:
    print("✗ Circe by Madeline Miller not found in database")
except Exception as e:
    print(f"✗ Error: {e}")
