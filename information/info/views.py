from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CreateUserForm, CustomerForm, EditProfileForm, TodoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django import forms


@unauthenticated_user
def home(request):

    context = {}

    return render(request, 'info/home.html', context)


@login_required(login_url='login')
def dashboard(request):
    # print(request.user)

    id = request.user.id
    form = TodoForm(initial={'author': id})

    item_list = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        form = TodoForm(request.POST, initial={'author': id})
        if form.is_valid():
            fm = form.save(commit=False)
            fm.author = request.user
            fm.save()
            return redirect('dashboard')

    page = {
            "forms": form,
            "list": item_list,
            "title": "TODO LIST",
        }
    return render(request, 'info/dashboard.html', page)


@login_required(login_url='login')
def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, "item removed !!!")
    return redirect('dashboard')


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'info/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'info/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    profile_form = EditProfileForm(instance=request.user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        profile_form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'info/account_settings.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'info/change_password.html', {
        'form': form
    })


def about(request):
    context = {}
    return render(request, 'info/about.html', context)