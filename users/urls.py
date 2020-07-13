from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("<int:pk>", views.user_view, name="user"),
    # path("login", views.LoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
]
