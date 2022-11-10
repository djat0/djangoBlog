from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class EditUserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    first_name = forms.CharField(label='first name', max_length=100)
    last_name = forms.CharField(label='last name', max_length=100)
    email = forms.CharField(label='email', max_length=100)


class ResetPassForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput, label='old password', max_length=100)
    new_password = forms.CharField(
        widget=forms.PasswordInput, label='new password', max_length=100)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label='confirm password', max_length=100)
