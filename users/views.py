from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import fields
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import AnagramForm, UserRegisterationForm, LoginForm
from django.contrib import messages
from django.views.generic import View
from django.views.generic import ListView
from .models import CustomUser


# Create your views here.


def register_user(request):
    if request.method == 'POST':
        rform = UserRegisterationForm(request.POST)

        if rform.is_valid():
            username = request.POST.get('username')
            messages.success(
                request, f'Account for {username} has been created successfully.')
            rform.save()
            return redirect('account:home')
    else:
        rform = UserRegisterationForm()
        return render(request, 'users/register.html', {'form': rform})
    return render(request, 'users/register.html', {'form': rform})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.data.get('password')
            print(request.POST)
            user = authenticate(request,
                                username=email, password=password)
            print(request.POST)
            print(email, password)
            print(user)
            if user:
                print('Got user')
                if user.check_password(password.strip()):
                    print('password match')
                    login(request, user)
                    return redirect('account:home')
            else:
                print('In Else statement')
                messages.warning(
                    request, 'Unable to login.\nwrong credentials')
            return render(request, 'users/login.html', {'form': form})
        return HttpResponse(request, 'gibresh')


# def login(request):
#     if request.method == "POST":
#         print(request.POST)
#     return render(request, 'users/login.html')


class AnagramView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/anagram.html')

    def post(self, request, *args, **kwargs):
        form = AnagramForm(request.POST)
        print(form.data)
        if form.is_valid():
            return HttpResponse(request, 'yes it is valid')
        return render(request, 'users/anagram.html', {'form': form})
