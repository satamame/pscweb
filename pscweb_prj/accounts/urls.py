from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /
    path('profile/', views.profile, name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]