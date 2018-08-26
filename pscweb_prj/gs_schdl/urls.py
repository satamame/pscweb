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
    # ex: /gs_schdl/0/mb/?idx=0
    path('<int:prod_id>/mb/', views.member, name='member'), # One member
    # ex: /gs_schdl/0/mb_list/
    path('<int:prod_id>/mb_list/', views.MemberListView.as_view(), name='mb_list'), # Member list
    # ex: /gs_schdl/0/tm/0/
    path('<int:prod_id>/tm/<int:team_id>', views.team, name='team'), # One team
    # ex: /gs_schdl/0/tm_list/
    path('<int:prod_id>/tm_list/', views.TeamListView.as_view(), name='tm_list'), # Team list

]
