from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form,
                                                       'section': 'login'})


def index(request):
    return render(request,
                  'account/index.html',
                  {'section': 'home'})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            registered = True
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user,
                           'registered': registered})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form,
                   'section': 'register'})

