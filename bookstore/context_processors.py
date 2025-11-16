"""
Context processors for the bookstore app.
"""


def cart_count(request):
    """Add cart count to all template contexts."""
    cart = request.session.get("cart", {})
    count = sum(cart.values()) if cart else 0
    return {"cart_count": count}
