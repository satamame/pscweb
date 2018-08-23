from django.contrib import admin
from .models import Production, Member, Team

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'prod_id')
    list_filter = ['prod_id']

admin.site.register(Production)
admin.site.register(Member, MemberAdmin)
admin.site.register(Team)
