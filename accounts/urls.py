from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /
    path('profile/', views.profile, name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(),
        name='user_create_complete'),
]
