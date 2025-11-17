"""
Context processors for the bookstore app.
"""


def cart_count(request):
    """Add cart count to all template contexts."""
    cart = request.session.get("cart", {})
    count = len(cart) if cart else 0
    return {"cart_count": count}


def wishlist_count(request):
    """Add wishlist count to all template contexts."""
    if request.user.is_authenticated:
        from .models import Wishlist

        count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {"wishlist_count": count}
