import os
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from django.views.generic import FormView, DetailView
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    views as auth_views,
    forms as auth_forms,
)
from django.http import Http404
from django.core.files.base import ContentFile
from django.contrib import messages

import requests

from . import models, forms
from django import forms as django_forms

# Create your views here.
class UserDetailView(DetailView):
    model = models.User
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello"
        return context


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
        return super().form_valid(form)"""


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
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
                return render(
                    self.request,
                    "users/verification_not_yet.html",
                    context={"user_id": user.pk},
                )
        else:
            print("login failed")
        return redirect(self.get_success_url())


def send_verify_view(request, user_id):
    try:
        user = models.User.objects.get(pk=user_id)
        user.verify_email()
        return render(
            request,
            "users/sending_verification.html",
            context={"email": user.email, "user_id": user.pk},
        )
    except models.User.DoesNotExist:
        return redirect("404.html")


# edit profile view
# url - users:edit
class UpdateProfileView(UpdateView):
    fields = (
        "email",
        "first_name",
        "last_name",
        "avatar",
        "bio",
        "gender",
        "currency",
        "language",
    )
    model = models.User
    template_name = "users/update-profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        user = models.User.objects.get(pk=self.request.user.pk)

        if email != user.email:
            # email(username) changed.
            try:
                # check if username is unique.
                models.User.objects.get(username=email)
                messages.error(
                    self.request,
                    "The email address you wrote is already exist. Use another please.",
                )
                return redirect(reverse("users:update"))

            except models.User.DoesNotExist:
                # case of username is unique.
                user.username = email
                user.email_verified = False
                print(user.username)
                user.login_method = models.User.LOGIN_METHOD_EMAIL
                user.save()
                user.verify_email()

                messages.info(
                    self.request,
                    f"We send a verification email to {email}. Please check your email for verification.",
                )

                return super().form_valid(form)
        else:
            # except email, other things are changed.
            return super().form_valid(form)


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
    messages.info(request, "Good by!")
    return redirect(reverse("core:home"))


# Signup Views
class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        form.save()
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            return render(
                self.request,
                "users/sending_verification.html",
                context={"email": user.email, "user_id": user.pk},
            )
        else:
            return redirect(self.get_success_url())


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

## Github Login
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
                            user = models.User.objects.get(username=email)

                            # todo: think about already exist email and git hub login method.

                            if (
                                user.email_verified is True
                                and user.login_method == models.User.LOGIN_METHOD_GITHUB
                            ):
                                login(request, user)
                                messages.success(
                                    request,
                                    f"Github login success, hello {user.first_name}.",
                                )
                                return redirect(reverse("core:home"))
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
                            messages.success(
                                request,
                                f"Github login success, hello {user.first_name}.",
                            )
                            return redirect(reverse("core:home"))
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
        messages.error(request, e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    auth_id = os.environ.get("KAKAO_AUTH_ID")
    auth_host = os.environ.get("KAKAO_AUTH_HOST")
    redirect_uri = "http://127.0.0.1:8000" + reverse("users:kakao_callback")

    redirect_to = (
        f"{auth_host}/oauth/authorize?client_id={auth_id}&redirect_uri={redirect_uri}"
        "&response_type=code"
    )

    return redirect(redirect_to)


def kakao_callback(request):
    auth_code = request.GET.get("code", None)
    try:
        if auth_code is not None:
            # Getting auth_code success
            auth_host = os.environ.get("KAKAO_AUTH_HOST") + "/oauth/token"
            auth_id = os.environ.get("KAKAO_AUTH_ID")
            redirect_uri = "http://127.0.0.1:8000" + reverse("users:kakao_callback")
            payloads = {
                "grant_type": "authorization_code",
                "client_id": auth_id,
                "redirect_uri": redirect_uri,
                "code": auth_code,
            }
            headers = {
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            }
            received = requests.post(auth_host, params=payloads, headers=headers)

            received_json = received.json()
            access_token = received_json.get("access_token", None)
            error = received_json.get("error", None)

            if error is None and access_token is not None:
                # continue using auth api which is the third step.
                api_url = os.environ.get("KAKAO_API_URL")
                user_info_url = api_url + "/v2/user/me"
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                }
                received = requests.post(user_info_url, headers=headers)
                received_json = received.json()
                kakao_account = received_json.get("kakao_account", None)

                if kakao_account is not None:
                    profile = kakao_account.get("profile")
                    email = kakao_account.get("email")
                    name = profile.get("nickname")
                    profile_url = profile.get("thumbnail_image_url")

                    name = name is not None and name or ""
                    profile_url = profile_url is not None and profile_url or ""

                    if email is None:
                        raise KakaoException(
                            "No information of email address in kakao profile. Cann't log in."
                        )

                    try:
                        # user has the github email is exist.
                        user = models.User.objects.get(username=email)

                        # todo: think about already exist email and git hub login method.

                        if (
                            user.email_verified is True
                            and user.login_method == models.User.LOGIN_METHOD_KAKAO
                        ):
                            login(request, user)
                            messages.success(
                                request, f"Login Success, hello {user.first_name}"
                            )
                            return redirect(reverse("core:home"))
                        else:
                            raise KakaoException(
                                "The kakao email that you logged in is already exist"
                                " and that user do not have kakao login method."
                            )
                    except models.User.DoesNotExist:
                        # no error getting kakao data.
                        # new user, we'll create user.
                        user = models.User.objects.create(
                            username=email, email=email, first_name=name
                        )

                        user.email_verified = True
                        user.login_method = models.User.LOGIN_METHOD_KAKAO
                        user.set_unusable_password()
                        user.save()
                        if profile_url is not None:
                            profile_request = requests.get(profile_url)
                            user.avatar.save(
                                f"{name}_{user.pk}_avatar",
                                ContentFile(profile_request.content),
                            )

                        login(request, user)
                        messages.success(
                            request, f"Login Success, hello {user.first_name}"
                        )
                        return redirect(reverse("core:home"))
                else:
                    raise KakaoException("Error in receiving profile from kakao.")
            else:
                raise KakaoException(error)
        else:
            # Failed to get auth_code
            error = request.GET.get("error", None)
            if error is not None:
                raise KakaoException(error)
            else:
                raise KakaoException(
                    "Failed to get auth code that is first step getting authorization."
                )
    except KakaoException as e:
        print("Failed to log in using kakao auth.")
        messages.error(request, e)
        print(e)
        return redirect(reverse("users:login"))

