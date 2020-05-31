from django import forms
from django.forms import ModelForm
from django.contrib.auth.admin import User
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ('username','password')

class PostModelForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title','body','picture')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name','last_name','email')

class ProfileModelForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('github_account_url','facebook_account_url','linkedIn_account_url','profile_pic')