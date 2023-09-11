from django.db import models

class Snapshot(models.Model):
    small_number = models.PositiveIntegerField()
    big_number = models.PositiveIntegerField()
    time = models.DateTimeField()
