from django.db import models

class Snapshot(models.Model):
    number = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
