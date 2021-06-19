from django.contrib.auth import tokens
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import LoginForm, UserRegistrationForm, MyPasswordResetForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# user password retireval
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def password_reset_request(request):
    link_expired = False
    if request.method == "POST":
        domain = request.headers['Host']
        password_reset_form = MyPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        "domain": domain,
                        "site_name": 'Borabams',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        'protocol':'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('password_reset_done')
    else:
        password_reset_form = MyPasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html",
    context={"password_reset_form": password_reset_form, 'section': 'password_reset'})            



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


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html', {'section': 'password_done'})

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html', {'section': 'password_complete'})