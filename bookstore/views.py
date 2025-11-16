from django.shortcuts import render
from .models import Book


def home(request):
    """View for the home page."""
    featured_books = Book.objects.filter(in_stock=True)[:6]
    context = {
        "featured_books": featured_books,
    }
    return render(request, "bookstore/home.html", context)


def fiction(request):
    """View for the fiction books page."""
    fiction_books = Book.objects.filter(category="fiction", in_stock=True)
    context = {
        "books": fiction_books,
        "category_title": "Fiction",
        "category_description": "Explore our collection of captivating fiction books.",
    }
    return render(request, "bookstore/category.html", context)


def nonfiction(request):
    """View for the non-fiction books page."""
    nonfiction_books = Book.objects.filter(category="nonfiction", in_stock=True)
    context = {
        "books": nonfiction_books,
        "category_title": "Non-Fiction",
        "category_description": "Discover knowledge and true stories in our non-fiction collection.",
    }
    return render(request, "bookstore/category.html", context)


def teens_kids(request):
    """View for the teens and kids books page."""
    teens_kids_books = Book.objects.filter(category="teens_kids", in_stock=True)
    context = {
        "books": teens_kids_books,
        "category_title": "Teens & Kids",
        "category_description": "Amazing books for young readers of all ages.",
    }
    return render(request, "bookstore/category.html", context)


def audiobooks(request):
    """View for the audiobooks page."""
    audiobooks_list = Book.objects.filter(category="audiobook", in_stock=True)
    context = {
        "books": audiobooks_list,
        "category_title": "Audiobooks",
        "category_description": "Listen to your favorite books on the go.",
    }
    return render(request, "bookstore/category.html", context)
