from django.db import models
from django.utils import timezone


class Book(models.Model):
    """Model representing a book in the bookstore."""

    CATEGORY_CHOICES = [
        ("fiction", "Fiction"),
        ("nonfiction", "Non-Fiction"),
        ("teens_kids", "Teens/Kids"),
        ("audiobook", "Audiobook"),
        ("toys_games", "Toys & Games"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    isbn = models.CharField(max_length=13, unique=True)
    cover_image = models.URLField(blank=True, null=True)
    publication_date = models.DateField()
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Order(models.Model):
    """Model representing a customer order."""

    DELIVERY_CHOICES = [
        ("delivery", "Home Delivery"),
        ("pickup", "Store Pickup"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("ready", "Ready for Pickup"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("completed", "Completed"),
    ]

    # Customer Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Delivery Information
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    # Order Information
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):
    """Model representing items in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"

    def get_subtotal(self):
        return self.quantity * self.price
