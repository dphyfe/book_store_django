from django.shortcuts import render
from .models import Book


def home(request):
    """View for the home page."""
    # Get The Shining by Stephen King
    stephen_king_book = Book.objects.filter(title="The Shining", author="Stephen King", in_stock=True).first()

    # Get other featured books from fiction and nonfiction only, excluding The Shining to avoid duplicates
    other_books = Book.objects.filter(category__in=["fiction", "nonfiction"], in_stock=True).exclude(id=stephen_king_book.id if stephen_king_book else None)[:7]

    # Combine them with The Shining first
    featured_books = [stephen_king_book] + list(other_books) if stephen_king_book else list(other_books)[:8]

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


def toys_games(request):
    """View for the toys and games page."""
    toys_games_list = Book.objects.filter(category="toys_games", in_stock=True)
    context = {
        "books": toys_games_list,
        "category_title": "Toys & Games",
        "category_description": "Fun toys and games for all ages.",
    }
    return render(request, "bookstore/category.html", context)


def cart(request):
    """View for the shopping cart page."""
    cart_items = request.session.get("cart", {})
    books_in_cart = []
    total_price = 0

    for book_id, quantity in cart_items.items():
        try:
            book = Book.objects.get(id=book_id)
            subtotal = float(book.price) * quantity
            books_in_cart.append({"book": book, "quantity": quantity, "subtotal": subtotal})
            total_price += subtotal
        except Book.DoesNotExist:
            pass

    context = {"cart_items": books_in_cart, "total_price": total_price, "cart_count": sum(cart_items.values())}
    return render(request, "bookstore/cart.html", context)


def add_to_cart(request, book_id):
    """Add a book to the shopping cart."""
    from django.shortcuts import redirect

    cart = request.session.get("cart", {})
    book_id_str = str(book_id)

    if book_id_str in cart:
        cart[book_id_str] += 1
    else:
        cart[book_id_str] = 1

    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER", "bookstore:home"))


def remove_from_cart(request, book_id):
    """Remove a book from the shopping cart."""
    from django.shortcuts import redirect

    cart = request.session.get("cart", {})
    book_id_str = str(book_id)

    if book_id_str in cart:
        del cart[book_id_str]

    request.session["cart"] = cart
    return redirect("bookstore:cart")


def book_detail(request, book_id):
    """View for individual book detail page."""
    from django.shortcuts import get_object_or_404

    book = get_object_or_404(Book, id=book_id)
    context = {
        "book": book,
    }
    return render(request, "bookstore/book_detail.html", context)
