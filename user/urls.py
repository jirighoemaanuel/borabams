from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PasswordResetConfirmForm
# app_name = 'blog'


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('', views.index, name='home'),
    # path('login/', auth_views.LoginView.as_view(get_form=LoginForm, redirect_authenticated_user='index.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    # reset password urls
    path('password_reset/',
        views.password_reset_request,
         name='password_reset'),
    path('password_reset/done/',
         views.password_reset_done,
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         views.password_reset_complete,
         name='password_reset_complete'),
]
