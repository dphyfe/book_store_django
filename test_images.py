import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Get featured books
shining = Book.objects.filter(title="The Shining", author="Stephen King", in_stock=True).first()
others = Book.objects.filter(category__in=["fiction", "nonfiction"], in_stock=True).exclude(id=shining.id if shining else None)[:7]
featured = [shining] + list(others) if shining else list(others)[:8]

print("Testing image URLs:\n")
for i, book in enumerate(featured, 1):
    print(f"{i}. {book.title}")
    print(f"   Image URL: {book.cover_image}")
    if book.cover_image:
        try:
            response = requests.head(book.cover_image, timeout=5)
            print(f"   Status: {response.status_code} {'✓ OK' if response.status_code == 200 else '✗ FAILED'}")
        except Exception as e:
            print(f"   Status: ✗ ERROR - {str(e)}")
    else:
        print(f"   Status: ✗ NO IMAGE URL")
    print()
