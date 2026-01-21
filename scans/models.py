from django.db import models
from django.contrib.auth.models import User
from targets.models import Target
from tools.models import Tool


class ScanTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scan_tasks')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tool.name} -> {self.target.name}"


class ScanResult(models.Model):
    scan_task = models.OneToOneField(ScanTask, on_delete=models.CASCADE, related_name='result')
    output = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Result for {self.scan_task.id}"

class Tool(models.Model):
    name = models.CharField(max_length=100)
    command_key = models.CharField(max_length=50)

    def __str__(self):
        return self.name
