from django.db import models


class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    command_key = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
