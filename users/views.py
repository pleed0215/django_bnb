from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout

from . import models, forms

# Create your views here.
def user_view(request, pk):
    pass


class LoginView(View):
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
        return render(request, "users/login.html", context={"forms": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("core:home"))


"""
위의 코드는
def login_view(request):
    if request.method == "get":
        pass
    elif request.method == "post":
        pass
와 동일하다.
"""
