from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username"]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # Set placeholders and classes for all fields
        self.fields["email"].widget.attrs.update(
            {"class": "form-control input-shadow", "placeholder": "Enter Email Address"}
        )
        self.fields["username"].widget.attrs.update(
            {"class": "form-control input-shadow", "placeholder": "Enter Username"}
        )

        # Handle password fields
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs.update(
                {"class": "form-control input-shadow", "placeholder": "Enter Password"}
            )
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update(
                {
                    "class": "form-control input-shadow",
                    "placeholder": "Confirm Password",
                }
            )
