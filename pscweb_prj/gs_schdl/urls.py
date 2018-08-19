from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /
    path('', views.prods, name='prods'), # Index of productions
]
