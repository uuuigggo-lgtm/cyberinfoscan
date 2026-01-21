from django.contrib import admin
from .models import Target


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_type', 'owner')
    list_filter = ('target_type', 'owner')
    search_fields = ('name',)
