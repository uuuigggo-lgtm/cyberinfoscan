from django.db import models
from django.contrib.auth.models import User


class Target(models.Model):
    TARGET_TYPES = (
        ('domain', 'Domain'),
        ('ip', 'IP Address'),
    )

    name = models.CharField(max_length=255)
    target_type = models.CharField(max_length=10, choices=TARGET_TYPES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='targets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
