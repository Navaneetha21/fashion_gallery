from django.db import models
from adminsapp.models import *



# Create your models here.
class Seller(models.Model):
    seller_id = models.CharField(max_length=100, primary_key=True)
    seller_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    created_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=100,default="pending")

    def __str__(self):
        return self.seller_name

    def generate_seller_id(self):
        pattern = "FG"
        sellers_pattern = Seller.objects.filter(seller_id__startswith=str(pattern))
        count = sellers_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.seller_id:
            self.seller_id = self.generate_seller_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "seller_table"


class Product(models.Model):
    product_id = models.CharField(max_length=10, primary_key=True)
    product_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    materials = models.CharField(max_length=100)
    pattern = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def generate_product_id(self):
        pattern = "FGPDT"
        product_pattern = Product.objects.filter(product_id__startswith=str(pattern))
        count = product_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = self.generate_product_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "product_table"


class Size(models.Model):
    size_id = models.CharField(max_length=10, primary_key=True)
    size = models.CharField(max_length=100)
    product_id = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)

    def __str__(self):
        return self.size_id

    def generate_size_id(self):
        pattern = "FGSZ"
        size_pattern = Size.objects.filter(size_id__startswith=str(pattern))
        count = size_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.size_id:
            self.size_id = self.generate_size_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "size_table"


class Image(models.Model):
    image_id = models.CharField(max_length=10, primary_key=True)
    product_id = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_file= models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image_id

    def generate_image_id(self):
        pattern = "FGIMG"
        image_pattern = Image.objects.filter(image_id__startswith=str(pattern))
        count = image_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.image_id:
            self.image_id = self.generate_image_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "image_table"

class Shirt(models.Model):
    shirt_id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name='shirts', on_delete=models.CASCADE)

    def __str__(self):
        return self.shirt_id

    def generate_shirt_id(self):
        pattern = "FGSRT"
        shirt_pattern = Shirt.objects.filter(shirt_id__startswith=str(pattern))
        count = shirt_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.shirt_id:
            self.shirt_id = self.generate_shirt_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "shirt_table"

class Kurta(models.Model):
    kurta_id = models.CharField(max_length=100, primary_key=True)
    quantity =models.IntegerField()
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name='kurtas', on_delete=models.CASCADE)

    def __str__(self):
        return self.kurta_id


    def generate_kurta_id(self):
        pattern = "FGKRT"
        kurta_pattern = Kurta.objects.filter(kurta_id__startswith=str(pattern))
        count = kurta_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.kurta_id:
            self.kurta_id = self.generate_kurta_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "kurta_table"

class Jeans(models.Model):
    jeans_id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name='jeans', on_delete=models.CASCADE)

    def __str__(self):
        return self.jeans_id


    def generate_jeans_id(self):
        pattern = "FGJNS"
        jeans_pattern = Jeans.objects.filter(jeans_id__startswith=str(pattern))
        count = jeans_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.jeans_id:
            self.jeans_id = self.generate_jeans_id()

        super().save(*args, **kwargs)

class Saree(models.Model):
    saree_id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name='sarees', on_delete=models.CASCADE)

    def __str__(self):
        return self.saree_id


    def generate_saree_id(self):
        pattern = "FGSRE"
        saree_pattern = Saree.objects.filter(saree_id__startswith=str(pattern))
        count = saree_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.saree_id:
            self.saree_id = self.generate_saree_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "saree_table"

class Tshirt(models.Model):
    tshirt_id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name='tshirts', on_delete=models.CASCADE)

    def __str__(self):
        return self.tshirt_id


    def generate_tshirt_id(self):
        pattern = "FGTSRT"
        tshirt_pattern = Tshirt.objects.filter(tshirt_id__startswith=str(pattern))
        count = tshirt_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.tshirt_id:
            self.tshirt_id = self.generate_tshirt_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "tshirt_table"

class Western(models.Model):
    western_id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name='westerns', on_delete=models.CASCADE)

    def __str__(self):
        return self.western_id


    def generate_western_id(self):
        pattern = "FGWST"
        western_pattern = Western.objects.filter(western_id__startswith=str(pattern))
        count = western_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.western_id:
            self.western_id = self.generate_western_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "western_table"

class Boysdrs(models.Model):
    boys_id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=100)
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name='boysdrss', on_delete=models.CASCADE)

    def __str__(self):
        return self.boys_id



    def generate_boys_id(self):
        pattern = "FGBD"
        boys_pattern = Shirt.objects.filter(boys_id__startswith=str(pattern))
        count = boys_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.boys_id:
            self.boys_id = self.generate_boys_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "boys_table"


class Offer(models.Model):
    offer_id=models.CharField(max_length=100,primary_key=True)
    discount=models.CharField(max_length=100)
    event_id=models.ForeignKey(Event, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,related_name='offer', on_delete=models.CASCADE)

    def __str__(self):
        return self.offer_id

    def generate_offer_id(self):
        pattern = "FGO"
        offer_pattern = Offer.objects.filter(offer_id__startswith=str(pattern))
        count = offer_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.offer_id:
            self.offer_id = self.generate_offer_id()

        super().save(*args, **kwargs)
    class Meta:
        db_table = "offer_table"

