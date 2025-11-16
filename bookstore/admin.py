from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "price", "in_stock"]
    list_filter = ["category", "in_stock"]
    search_fields = ["title", "author", "isbn"]
    ordering = ["title"]
