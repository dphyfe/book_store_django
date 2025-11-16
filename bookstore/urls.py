from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path("", views.home, name="home"),
    path("fiction/", views.fiction, name="fiction"),
    path("nonfiction/", views.nonfiction, name="nonfiction"),
    path("teens-kids/", views.teens_kids, name="teens_kids"),
    path("audiobooks/", views.audiobooks, name="audiobooks"),
    path("toys-games/", views.toys_games, name="toys_games"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:book_id>/", views.remove_from_cart, name="remove_from_cart"),
]
