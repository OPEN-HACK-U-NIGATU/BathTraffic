from django.db import models

class Snapshot(models.Model):
    small_number = models.PositiveIntegerField()
    big_number = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    image_path = models.ImageField(upload_to="image/")
    upload_at = models.DateTimeField(auto_now_add=True)

