from django.urls import path
from . import views

app_name = 'gs_schdl'
urlpatterns = [
    # ex: /gs_schdl/
    path('', views.ProductionIndexView.as_view(), name='prod_index'), # Index of productions
    # ex: /gs_schdl/0/
    path('<int:prod_id>/', views.schedule, name='schedule'), # Schedule summary
]
