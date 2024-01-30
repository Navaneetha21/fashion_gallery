from django.db import models
from sellerapp.models import *

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    user_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    create_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=100,default="Active")

    def generate_user_id(self):
        pattern = "FG"
        user_pattern = User.objects.filter(user_id__startswith=str(pattern))
        count = user_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_user_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "user_table"

class Cart(models.Model):
    cart_id = models.CharField(max_length=10, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='cart', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def generate_cart_id(self):
        pattern = "FGCT"
        cart_pattern = Cart.objects.filter(cart_id__startswith=str(pattern))
        count = cart_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.cart_id:
            self.cart_id = self.generate_cart_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "cart_table"

# class Address(models.Model):
#     address_id = models.AutoField(primary_key=True)
#     house_name = models.CharField(max_length=100)
#     city_name = models.CharField(max_length=100)
#     landmark = models.CharField(max_length=100)
#     district =
#     state =
#     post_office = models.CharField(max_length=100)
#     pin = models.IntegerField()
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "address_table"
#
# class Review(models.Model):
#     review_id = models.AutoField(primary_key=True)
#     review = models.CharField(max_length=100)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "review_table"
