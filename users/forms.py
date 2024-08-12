from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class RegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "birthday",
            "email",
            "phone",
            "password1",
            "password2",
        )


class UserForm(StyleFormMixin, UserChangeForm):
    pass

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "birthday",
            "email",
            "password",
            "telegram",
            "phone",
            "avatar",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()
