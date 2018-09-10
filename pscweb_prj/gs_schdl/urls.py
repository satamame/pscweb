from django.urls import path
from . import views

app_name = 'gs_schdl'
urlpatterns = [
    # ex: /gs_schdl/
    path('', views.ProductionIndexView.as_view(), name='prod_index'), # Index of productions
    # ex: /gs_schdl/1/
    path('<int:prod_id>/', views.schedule, name='schedule'), # Schedule summary for production
    # ex: /gs_schdl/1/rh/1/
    path('<int:prod_id>/rh/<int:rh_idx>/', views.rehearsal, name='rehearsal'), # One rehearsal
    
    # ex: /gs_schdl/1/mb/?{idx=1|id=1}
    path('<int:prod_id>/mb/', views.member, name='member'), # One member
    # ex: /gs_schdl/1/mb_list/
    path('<int:prod_id>/mb_list/', views.MemberListView.as_view(), name='mb_list'), # Member list
    # ex: /gs_schdl/1/tm/1/
    path('<int:prod_id>/tm/<int:team_id>/', views.team, name='team'), # One team
    # ex: /gs_schdl/1/tm_list/[?mbid=1]
    path('<int:prod_id>/tm_list/', views.TeamListView.as_view(), name='tm_list'), # Team list
    
    # ex: /gs_schdl/1/rh_list/
    path('<int:prod_id>/rh_list/', views.RhListView.as_view(), name='rh_list'), # Rehearsal list
    # ex: /gs_schdl/rh_tm/1/
    path('rh_tm/<int:rhplan_id>/', views.rh_teams, name='rh_teams'), # Team table per Rehearsal

    # ex: /gs_schdl/rp/1/
    path('rp/<int:rhplan_id>/', views.rhplan, name='rhplan'), # Rehearsal Plan
    # ex: /gs_schdl/rp/1/edit/
    path('rp/<int:rhplan_id>/edit/', views.rp_edit, name='rp_edit'), # Rehearsal Plan Edit
    # ex: /gs_schdl/1/rp_list/
    path('<int:prod_id>/rp_list/', views.RhPlanListView.as_view(), name='rp_list'), # Rehearsal Plan list
    

]
