import uuid

from django.db import models
from sellerapp.models import *
from django.contrib.auth.models import User
import uuid
# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    user_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    create_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=100,default="Active")

    def __str__(self):
        return self.user_name

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

    def __str__(self):
        return self.cart_id

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


class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=10, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='wishlist', on_delete=models.CASCADE)

    def __str__(self):
        return self.wishlist_id

    def generate_wishlist_id(self):
        pattern = "FGWL"
        wishlist_pattern = Wishlist.objects.filter(wishlist_id__startswith=str(pattern))
        count = wishlist_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.wishlist_id:
            self.wishlist_id = self.generate_wishlist_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "wishlist_table"
class Address(models.Model):
    address_id = models.CharField(max_length=10, primary_key=True)
    house_name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    pin = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.address_id

    def generate_address_id(self):
        pattern = "FGAD"
        address_pattern = Address.objects.filter(address_id__startswith=str(pattern))
        count = address_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.address_id:
            self.address_id = self.generate_address_id()

        super().save(*args, **kwargs)
    class Meta:
        db_table = "address_table"

class Review(models.Model):
    review_id = models.CharField(max_length=10, primary_key=True)
    review = models.TextField(max_length=100)
    product_id = models.ForeignKey(Product, related_name='review', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.review_id

    def generate_review_id(self):
        pattern = "FGRV"
        review_pattern = Review.objects.filter(review_id__startswith=str(pattern))
        count = review_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.review_id:
            self.review_id = self.generate_review_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "review_table"

class Order(models.Model):
    order_id = models.CharField(max_length=10, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True)
    address_id = models.ForeignKey(Address,  on_delete=models.CASCADE)
    ordered_date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, default="Pending")

    def __str__(self):
        return self.order_id

    def generate_order_id(self):
        pattern = "FGOD"
        order_pattern = Order.objects.filter(order_id__startswith=str(pattern))
        count = order_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "order_table"

# class Payment(models.Model):
#     payment_id = models.CharField(max_length=10, primary_key=True)
#     payment_type = models.CharField(max_length=100)
#     date = models.DateField(autonow=True)
#     time = models.TimeField(autonow=True)
#     order_id = models.ForeignKey(Order,  on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.payment_id
#
#     def generate_payment_id(self):
#         pattern = "FGP"
#         payment_pattern = Payment.objects.filter(payment_id__startswith=str(pattern))
#         count = payment_pattern.count() + 1
#         return f"{pattern}-{count:03d}"
#
#     def save(self, *args, **kwargs):
#         if not self.payment_id:
#             self.payment_id = self.generate_payment_id()
#
#         super().save(*args, **kwargs)
#
#     class Meta:
#         db_table = "payment_table"

# class Profile(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
#     phone_number=models.CharField(max_length=100)
#     otp=models.CharField(max_length=100, null=True, blank=True)
#     uid = models.UUIDField(default=uuid.uuid4)