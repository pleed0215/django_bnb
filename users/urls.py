from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("<int:pk>/", views.UserDetailView.as_view(), name="user"),
    path("favorite/", views.FavoriteView.as_view(), name="favorite"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
    path("<int:user_id>/send_verify/",
         views.send_verify_view, name="send-verify"),
    # path("login", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("verify/<str:key>/", views.complete_verification, name="verify"),
    path("login/github/", views.github_login, name="github"),
    path("login/github/callback/", views.github_callback, name="github_callback"),
    path("login/kakao/", views.kakao_login, name="kakao"),
    path("login/kakao/callback", views.kakao_callback, name="kakao_callback"),
    path("start-host/", views.switch_host, name="switch_host"),
    path("switch-language/", views.switch_language, name="switch_lang"),
]
