from django.urls import path
from . import views

app_name = 'scripts'
urlpatterns = [
    # ex: /scripts/
    path('', views.scripts, name='sc_index'), # Index of scripts
    # ex: /scripts/convert/
    path('convert/', views.convert, name='sc_convert'), # Script Converter
]
