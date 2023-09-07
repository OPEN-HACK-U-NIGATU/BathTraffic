from django.db import models

class Snapshot(models.Model):
    number = models.PositiveIntegerField()
    time = models.TimeField()
