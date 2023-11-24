from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "id": "username", "name": "username"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "id": "password1", "name": "password1"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "id": "password2", "name": "password1"}
        )

    email = forms.EmailField(
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "name": "email",
                "id": "email-input",
            }
        ),
    )

    first_name = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "name": "first_name",
                "id": "first_name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "name": "last_name",
                "id": "last_name",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "id": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "id": "password"}
        )


class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "id": "first_name"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "id": "last_name"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "id": "email"}
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class PasswordEditForm(forms.Form):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        required=False,
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "id": "password1",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        required=False,
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "id": "password2",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
