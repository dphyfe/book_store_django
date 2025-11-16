from django.urls import path
from . import views

app_name = "bookstore"

urlpatterns = [
    path("", views.home, name="home"),
    path("fiction/", views.fiction, name="fiction"),
    path("nonfiction/", views.nonfiction, name="nonfiction"),
    path("teens-kids/", views.teens_kids, name="teens_kids"),
    path("audiobooks/", views.audiobooks, name="audiobooks"),
]
