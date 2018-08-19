from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /
    path('', views.ProductionIndexView.as_view(), name='prod_index'), # Index of productions
]
