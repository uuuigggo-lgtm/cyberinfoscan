from django.contrib import admin
from .models import ScanTask, ScanResult, Tool


@admin.register(ScanTask)
class ScanTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'tool',
        'target',
        'status',
        'created_at',
    )
    list_filter = ('status', 'tool', 'user')
    search_fields = ('target__name', 'user__username')
    ordering = ('-created_at',)


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'scan_task', 'short_output')

    def short_output(self, obj):
        return obj.output[:60]

    short_output.short_description = 'Result Preview'


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'command_key')
