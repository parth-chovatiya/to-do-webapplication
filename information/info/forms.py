from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"
        exclude = ['author']


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['name', 'user', 'email']


class EditProfileForm(ModelForm):
    date_joined = forms.CharField(disabled=True)
    last_login = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'last_login']
