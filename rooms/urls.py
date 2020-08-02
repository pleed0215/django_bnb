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
    path("<int:pk>/update/", views.UpdateRoomView.as_view(), name="update"),
    path("<int:pk>/photos/", views.EditPhotosView.as_view(), name="photos"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete_photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit_photo",
    ),
    path("search/", views.search_view, name="search"),
]

