# Database schemas intialized.
from django.db import models

class Data(models.Model):
    time = models.CharField(max_length=10)
    price = models.IntegerField()