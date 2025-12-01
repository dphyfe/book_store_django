from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "bookstore"

router = DefaultRouter()
router.register(r"books", views.BookViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("fiction/", views.fiction, name="fiction"),
    path("nonfiction/", views.nonfiction, name="nonfiction"),
    path("teens-kids/", views.teens_kids, name="teens_kids"),
    path("audiobooks/", views.audiobooks, name="audiobooks"),
    path("toys-games/", views.toys_games, name="toys_games"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:book_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Account Management
    path("account/", views.manage_account, name="manage_account"),
    path("account/orders/", views.order_status_view, name="order_status"),
    path("account/addresses/", views.address_book, name="address_book"),
    path("account/addresses/add/", views.add_address, name="add_address"),
    path("account/addresses/edit/<int:address_id>/", views.edit_address, name="edit_address"),
    path("account/addresses/delete/<int:address_id>/", views.delete_address, name="delete_address"),
    path("account/payments/", views.payment_methods_view, name="payment_methods"),
    path("account/payments/add/", views.add_payment, name="add_payment"),
    path("account/payments/delete/<int:payment_id>/", views.delete_payment, name="delete_payment"),
    # Wishlist
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/add/<int:book_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:book_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
]
