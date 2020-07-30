from django.urls import path, include
from . import views

app_name = "rooms"

"""
urlpatterns = [
    path("<int:pk>", views.detail_view, name="detail"),
]
"""

urlpatterns = [
    path("<int:pk>/", views.RoomDetailView.as_view(), name="detail"),
    path("<int:pk>/update", views.UpdateRoomView.as_view(), name="update"),
    path("search/", views.search_view, name="search"),
]

