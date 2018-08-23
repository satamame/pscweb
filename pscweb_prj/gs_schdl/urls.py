from django.urls import path
from . import views

app_name = 'gs_schdl'
urlpatterns = [
    # ex: /gs_schdl/
    path('', views.ProductionIndexView.as_view(), name='prod_index'), # Index of productions
    # ex: /gs_schdl/0/
    path('<int:prod_id>/', views.schedule, name='schedule'), # Schedule summary for production
    # ex: /gs_schdl/0/rh/0/
    path('<int:prod_id>/rh/<int:rh_idx>/', views.rehearsal, name='rehearsal'), # One rehearsal
    # ex: /gs_schdl/0/ps/?idx=0
    path('<int:prod_id>/ps/', views.person, name='person'), # One person

]
