import os
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

import requests

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

# Social login part
class GithubException(Exception):
    pass


def github_login(request):
    # need to view
    # https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps

    auth_id = os.environ.get("GITHUB_AUTH_ID")

    callback = f'http://127.0.0.1:8000{reverse_lazy("users:github_callback")}'
    auth_to = os.environ.get("GITHUB_REDIRECT")
    scope = "read:user"  # only read github users profil.

    auth_to = f"{auth_to}?client_id={auth_id}&redirect_uri={callback}&scope={scope}"

    return redirect(auth_to)


def github_callback(request):
    code = request.GET.get("code", None)

    try:
        if code is not None:
            auth_id = os.environ.get("GITHUB_AUTH_ID")
            auth_secret = os.environ.get("GITHUB_AUTH_SECRET")
            auth_to = os.environ.get("GITHUB_POST_URL")
            callback = f'http://127.0.0.1:8000{reverse_lazy("users:github_callback")}'
            receive = requests.post(
                auth_to,
                data={
                    "client_id": auth_id,
                    "client_secret": auth_secret,
                    "code": code,
                    "redirect_uri": callback,
                },
                headers={"Accept": "application/json",},
            )
            if receive:
                result_json = receive.json()
                error = result_json.get("error", None)
                if error is not None:
                    # there is an error getting github login information.
                    print("Error occured in github login.")
                    raise GithubException(
                        f"Error occured in getting github access_token"
                        f"\nError Message: {error}"
                    )
                else:
                    auth_token = result_json.get("access_token", None)
                    api_url = os.environ.get("GITHUB_API_URL")
                    user_from_github = requests.get(
                        api_url,
                        headers={
                            "Accept": "application/json",
                            "Authorization": f"token {auth_token}",
                        },
                    )

                    github_user = user_from_github.json()
                    username = github_user.get("login", None)

                    if username is not None:
                        name = github_user.get("name")
                        email = github_user.get("email")
                        bio = github_user.get("bio")

                        name = name is not None and name or ""
                        bio = bio is not None and bio or "No bio"

                        if email is None:
                            raise GithubException(
                                "No information of email address in github profile. Cann't log in."
                            )

                        try:
                            # user has the github email is exist.
                            user = models.User.objects.get(email=email)

                            # todo: think about already exist email and git hub login method.

                            if (
                                user.email_verified is True
                                and user.login_method == models.User.LOGIN_METHOD_GITHUB
                            ):
                                login(request, user)
                            else:
                                raise GithubException(
                                    "The github email that you logged in is already exist"
                                    "and that user do not have github login method."
                                )
                        except models.User.DoesNotExist:
                            # no error getting github data.
                            # new user, we'll create user.
                            user = models.User.objects.create(
                                username=email, bio=bio, email=email, first_name=name
                            )
                            user.email_verified = True
                            user.login_method = models.User.LOGIN_METHOD_GITHUB
                            user.set_unusable_password()
                            user.save()
                            login(request, user)
                    else:
                        raise GithubException(
                            "Error in receiving username on github profile."
                        )
            else:
                # while getting code from github auth page, error occured.
                raise GithubException("Cannot retrive code from ")
        else:
            # while getting code from github auth page, error occured.
            raise GithubException("While getting code, error occured.")
    except GithubException as e:
        print(e)
        return redirect(reverse("users:login"))
    finally:
        print("Success getting github login data.")
        return redirect(reverse("core:home"))


def kakao_login(request):
    pass


def kakao_callback(request):
    pass
