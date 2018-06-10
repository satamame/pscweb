from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm

@login_required
def profile(request):
    return HttpResponse("Hello, {}.".format(request.user.username))


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
