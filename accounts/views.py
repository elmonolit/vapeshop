from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('sign_in')


class SignInView(LoginView):
    template_name = 'sign_in.html'
    success_url = reverse_lazy('index')


class SignOutView(LogoutView):
    success_url = reverse_lazy('sign_in')
