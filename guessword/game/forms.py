from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "role")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not (any(c.islower() for c in username) and any(c.isupper() for c in username)):
            raise ValidationError("Username must include both uppercase and lowercase letters.")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 5:
            raise ValidationError("Password must be at least 5 characters long.")
        if not re.search(r"[A-Za-z]", password):
            raise ValidationError("Password must contain at least one letter.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r"[$%@*]", password):
            raise ValidationError("Password must contain at least one special char ($, %, *, @).")
        return password


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
