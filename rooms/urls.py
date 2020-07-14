from django.urls import path, include
from . import views

app_name = "rooms"

"""
urlpatterns = [
    path("<int:pk>", views.detail_view, name="detail"),
]
"""

urlpatterns = [
    path("<int:pk>", views.RoomDetailView.as_view(), name="detail"),
    path("search", views.search_view, name="search"),
]

