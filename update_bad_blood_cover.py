import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Update Bad Blood book with cover image
try:
    book = Book.objects.get(title="Bad Blood", author="John Carreyrou")
    book.cover_image = "https://i5.walmartimages.com/seo/Bad-Blood-Secrets-and-Lies-in-a-Silicon-Valley-Startup-Hardcover-by-John-Carreyrou-9781509868063_38499bee-bf0b-4470-a988-4bc71d1fb64f.a099cd3891dc7890c7434fe16de8439f.jpeg"
    book.save()
    print(f"\u2713 Successfully updated cover image for '{book.title}' by {book.author}")
except Book.DoesNotExist:
    print("\u2717 Bad Blood by John Carreyrou not found in database")
except Exception as e:
    print(f"\u2717 Error: {e}")
