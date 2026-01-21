from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from targets.models import Target
from scans.models import ScanTask


class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_active',
        'targets_count',
        'scans_count',
    )

    def targets_count(self, obj):
        return Target.objects.filter(owner=obj).count()

    def scans_count(self, obj):
        return ScanTask.objects.filter(user=obj).count()

    targets_count.short_description = 'Targets'
    scans_count.short_description = 'Scans'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
