from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
]