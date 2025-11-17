from django.contrib import admin
from .models import Book, Order, OrderItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "price", "in_stock"]
    list_filter = ["category", "in_stock"]
    search_fields = ["title", "author", "isbn"]
    ordering = ["title"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["book", "quantity", "price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "delivery_method", "total_amount", "status", "created_at"]
    list_filter = ["status", "delivery_method", "created_at"]
    search_fields = ["first_name", "last_name", "email", "phone"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [OrderItemInline]
    ordering = ["-created_at"]
