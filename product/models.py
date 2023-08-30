from django.db import models
from users.models import Seller, Customer
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Rate(models.Model):
    rate = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def __str__(self):
        return str(self.rate)


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.IntegerField(null=False, default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    comment_content = models.TextField()
    comment_rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.comment_author} on {self.product}"


class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.customer.name} - Created at {self.created_at}'


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    many = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.many} {self.product.name}(s) in {self.basket}'
