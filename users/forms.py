from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

# Custom create user form and custom update user form
# Using email instead of username


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', )
