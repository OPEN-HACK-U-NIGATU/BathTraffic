from django.db import models

class Snapshot(models.Model):
    small_number = models.PositiveIntegerField()
    big_number = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)

class Prediction(models.Model):
    p_small_number = 
    p_big_number = 
    time = 

