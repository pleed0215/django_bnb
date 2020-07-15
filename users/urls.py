from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("<int:pk>", views.user_view, name="user"),
    # path("login", views.LoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("verify/<str:key>", views.complete_verification, name="verify"),
    path("login/github", views.github_login, name="github"),
    path("login/github/callback", views.github_callback, name="github_callback"),
    path("login/kakao", views.kakao_login, name="kakao"),
    path("login/kakao/callback", views.kakao_callback, name="kakao_callback"),
]
