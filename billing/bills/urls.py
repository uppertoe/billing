from django.urls import path

from . import views

urlpatterns = [
    path("bills/create", views.create_case, name="create_case"),
    path("bills/all", views.ProfileListView.as_view(), name="profile_list"),
    path("bills", views.CaseListView.as_view(), name="case_list"),
    path("ajax/search-items", views.search_items, name="search_items"),
    path("ajax/search-items/<str:category>", views.search_items, name="search_items_category"),
]
