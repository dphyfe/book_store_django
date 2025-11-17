from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Address, PaymentMethod, Order, Wishlist
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, AddressForm, PaymentMethodForm


def search(request):
    """View for search results."""
    query = request.GET.get("q", "")
    books = []

    if query:
        from django.db.models import Q

        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)).filter(in_stock=True)

    context = {
        "books": books,
        "query": query,
        "category_title": f"Search Results for '{query}'" if query else "Search",
        "category_description": f"Found {books.count()} results" if query else "Enter a search term to find books",
    }
    return render(request, "bookstore/category.html", context)


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
    cart = request.session.get("cart", {})
    book_id_str = str(book_id)

    if book_id_str in cart:
        del cart[book_id_str]

    request.session["cart"] = cart
    return redirect("bookstore:cart")


def book_detail(request, book_id):
    """View for individual book detail page."""
    book = get_object_or_404(Book, id=book_id)
    context = {
        "book": book,
    }
    return render(request, "bookstore/book_detail.html", context)


def checkout(request):
    """View for the checkout page."""
    from .models import OrderItem

    cart = request.session.get("cart", {})
    if not cart:
        return redirect("bookstore:cart")

    # Calculate cart details
    books_in_cart = []
    total_price = 0
    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            subtotal = float(book.price) * quantity
            books_in_cart.append({"book": book, "quantity": quantity, "subtotal": subtotal})
            total_price += subtotal
        except Book.DoesNotExist:
            pass

    if request.method == "POST":
        # Create order
        order = Order.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            delivery_method=request.POST.get("delivery_method"),
            address=request.POST.get("address", ""),
            city=request.POST.get("city", ""),
            state=request.POST.get("state", ""),
            zip_code=request.POST.get("zip_code", ""),
            total_amount=total_price,
            notes=request.POST.get("notes", ""),
        )

        # Create order items
        for item in books_in_cart:
            OrderItem.objects.create(
                order=order,
                book=item["book"],
                quantity=item["quantity"],
                price=item["book"].price,
            )

        # Clear cart
        request.session["cart"] = {}

        return redirect("bookstore:order_confirmation", order_id=order.id)

    context = {
        "cart_items": books_in_cart,
        "total_price": total_price,
    }
    return render(request, "bookstore/checkout.html", context)


def order_confirmation(request, order_id):
    """View for order confirmation page."""
    order = get_object_or_404(Order, id=order_id)
    context = {
        "order": order,
    }
    return render(request, "bookstore/order_confirmation.html", context)


# Authentication Views
def register_view(request):
    """User registration view."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to Burt's Bookshelf!")
            return redirect("bookstore:home")
    else:
        form = RegisterForm()
    return render(request, "bookstore/register.html", {"form": form})


def login_view(request):
    """User login view."""
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect("bookstore:home")
    else:
        form = LoginForm()
    return render(request, "bookstore/login.html", {"form": form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("bookstore:home")


@login_required
def manage_account(request):
    """View for managing user account."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("bookstore:manage_account")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "bookstore/manage_account.html", {"form": form})


@login_required
def order_status_view(request):
    """View for viewing user's orders."""
    orders = Order.objects.filter(email=request.user.email).order_by("-created_at")
    return render(request, "bookstore/order_status.html", {"orders": orders})


@login_required
def address_book(request):
    """View for managing user addresses."""
    addresses = Address.objects.filter(user=request.user)
    return render(request, "bookstore/address_book.html", {"addresses": addresses})


@login_required
def add_address(request):
    """View for adding a new address."""
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect("bookstore:address_book")
    else:
        form = AddressForm()
    return render(request, "bookstore/address_form.html", {"form": form})


@login_required
def edit_address(request, address_id):
    """View for editing an address."""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            updated_address = form.save(commit=False)
            if updated_address.is_default:
                Address.objects.filter(user=request.user, is_default=True).exclude(id=address_id).update(is_default=False)
            updated_address.save()
            messages.success(request, "Address updated successfully!")
            return redirect("bookstore:address_book")
    else:
        form = AddressForm(instance=address)
    return render(request, "bookstore/address_form.html", {"form": form, "address": address})


@login_required
def delete_address(request, address_id):
    """View for deleting an address."""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Address deleted successfully!")
    return redirect("bookstore:address_book")


@login_required
def payment_methods_view(request):
    """View for managing payment methods."""
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    return render(request, "bookstore/payment_methods.html", {"payment_methods": payment_methods})


@login_required
def add_payment(request):
    """View for adding a payment method."""
    if request.method == "POST":
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            if payment.is_default:
                PaymentMethod.objects.filter(user=request.user, is_default=True).update(is_default=False)
            payment.save()
            messages.success(request, "Payment method added successfully!")
            return redirect("bookstore:payment_methods")
    else:
        form = PaymentMethodForm()
    return render(request, "bookstore/payment_form.html", {"form": form})


@login_required
def delete_payment(request, payment_id):
    """View for deleting a payment method."""
    payment = get_object_or_404(PaymentMethod, id=payment_id, user=request.user)
    payment.delete()
    messages.success(request, "Payment method removed successfully!")
    return redirect("bookstore:payment_methods")


@login_required
def wishlist_view(request):
    """View for displaying user's wishlist."""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("book")
    return render(request, "bookstore/wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def add_to_wishlist(request, book_id):
    """Add a book to the wishlist."""
    book = get_object_or_404(Book, id=book_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, f"{book.title} added to your wishlist!")
    else:
        messages.info(request, f"{book.title} is already in your wishlist.")
    return redirect(request.META.get("HTTP_REFERER", "bookstore:home"))


@login_required
def remove_from_wishlist(request, book_id):
    """Remove a book from the wishlist."""
    wishlist_item = get_object_or_404(Wishlist, user=request.user, book_id=book_id)
    book_title = wishlist_item.book.title
    wishlist_item.delete()
    messages.success(request, f"{book_title} removed from your wishlist.")
    return redirect("bookstore:wishlist")
