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


# Let's make ModelFrom version.
class SignupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        print(password)
        print(password2)
        if password == password2:
            return password2
        else:
            forms.ValidationError("Password is not match each other.")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            models.User.objects.get(username=email)
            raise forms.ValidationError(
                f"{email} is already exist. Use another please."
            )
        except models.User.DoesNotExist:
            return email

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = super().save(commit=False)
        user.username = email
        user.set_password(password)
        user.save()


"""class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.EmailField(help_text="Write as email")
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    def clean_username(self):
        username = self.cleaned_data.get("username")

        try:
            models.User.objects.get(username=username)
            raise forms.ValidationError(
                f"{username} is already exist. Use another please."
            )
        except models.User.DoesNotExist:
            return username

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password is password2:
            return password2

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(
            username,
            email=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.save()

    # clean method 하나로 통일.

    def clean_email(self):
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
