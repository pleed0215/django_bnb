from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    views as auth_views,
    forms as auth_forms,
)
from django.http import Http404

from . import models, forms

# Create your views here.
def user_view(request, pk):
    pass


# Login Views
"""class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            print("login success")
            login(self.request, user)
            return redirect(reverse("core:home"))
        else:
            print("login failed")
        return super().form_valid(form)
"""


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    authentication_form = auth_forms.AuthenticationForm
    success_url = reverse_lazy("core:home")
    redirect_authenticated_user = True

    def form_valid(self, form):
        email = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            if user.email_verified is True:
                print("login success")
                login(self.request, user)
                return redirect(reverse("core:home"))
            else:
                return render(self.request, "users/verification_not_yet.html")
        else:
            print("login failed")
        return redirect(self.get_success_url())


# login form page, using just View Class.
"""class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html", context={"forms": forms.LoginForm()})

    def post(self, request):
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                print("login success")
                login(request, user)
                return redirect(reverse("core:home"))
            else:
                print("login failed")
        else:
            print("data validation error")
        print(form.cleaned_data)
        return render(request, "users/login.html", context={"form": form})"""


def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


# Signup Views
class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        if form.is_valid():
            print("valid")
        form.save()
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            return render(
                self.request,
                "users/sending_verification.html",
                context={"email": user.email},
            )
        else:
            print("login failed")
        return super().form_valid(form)


def complete_verification(request, key):
    is_success = False
    print(key)
    try:
        user = models.User.objects.get(email_secret=key)
        if user is not None:
            user.email_verified = True
            user.save()
            is_success = True
        print("success")

    except models.User.DoesNotExist as e:
        print(e)
        is_success = False
        print("failed")

    finally:
        return render(
            request, "users/verification.html", context={"success": is_success}
        )


"""
위의 코드는
def login_view(request):
    if request.method == "get":
        pass
    elif request.method == "post":
        pass
와 동일하다.
"""
