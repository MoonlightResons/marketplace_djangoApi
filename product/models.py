from django.db import models
from users.models import Seller, Customer


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.IntegerField(null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


