from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fiel
