from django.contrib import admin
from .models import Production, Member, Team, RhPlan

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'prod_id')
    list_filter = ['prod_id']

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'prod_id')
    list_filter = ['prod_id']

class RhPlanAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'prod_id')
    list_filter = ['prod_id']
    ordering = ['sort_key']

admin.site.register(Production)
admin.site.register(Member, MemberAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(RhPlan, RhPlanAdmin)
