import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burts_books.settings")
django.setup()

from bookstore.models import Book

# Check what appears on home page
shining = Book.objects.filter(title="The Shining", author="Stephen King", in_stock=True).first()
print(f"1. The Shining - Image: {shining.cover_image if shining else 'NOT FOUND'}")

others = Book.objects.filter(category__in=["fiction", "nonfiction"], in_stock=True).exclude(id=shining.id if shining else None)[:7]

print("\nOther 7 books on home page:")
for i, b in enumerate(others):
    print(f"{i + 2}. {b.title} ({b.category}) - Image: {'YES' if b.cover_image else 'NO'}")
