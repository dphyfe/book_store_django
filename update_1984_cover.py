import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Update 1984 book with cover image
try:
    book = Book.objects.get(title__icontains="1984")
    book.cover_image = "https://target.scene7.com/is/image/Target/GUEST_0c931564-881c-4622-8594-1d08076fed97?wid=300&hei=300&fmt=pjpeg"
    book.save()
    print(f"✓ Successfully updated cover image for '{book.title}' by {book.author}")
except Book.DoesNotExist:
    print("✗ 1984 not found in database")
except Exception as e:
    print(f"✗ Error: {e}")
