from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            users = models.User.objects.get(username=email)
            if users and users.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    "password",
                    forms.ValidationError("Password is not matched for that user."),
                )
        except models.User.DoesNotExist as e:
            print(e)
            self.add_error(
                "email",
                forms.ValidationError("User has that email address doesn't exist."),
            )

    # clean method 하나로 통일.
    """def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist as e:
            print(e)
            raise forms.ValidationError("User has that email address doesn't exist.")

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            users = models.User.objects.get(username=email)
            if users and users.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is not matched for that user.")
        except models.User.DoesNotExist as e:
            print(e)
            raise forms.ValidationError("User has that email address doesn't exist.")"""
