from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date = models.DateTimeField()