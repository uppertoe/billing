from django.urls import path

from . import views

urlpatterns = [
    path("ajax/search-items", views.get_items, name="search_items"),
    path("ajax/search-items/<str:category>", views.get_items, name="search_items_category"),
]
