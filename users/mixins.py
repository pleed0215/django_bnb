from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages

from . import models


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated == True
            and self.request.user.login_method == models.User.LOGIN_METHOD_EMAIL
        )

    def handle_no_permission(self):
        messages.error(self.request, "Only email loggin user can go there")
        return redirect(reverse("core:home"))


class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "user who logged in can't go there.")
        return redirect(reverse("core:home"))


# if not loggin, move to login_url
class LoginOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

    def handle_no_permission(self):
        messages.error(self.request, "You need to login")
        return super().handle_no_permission()
