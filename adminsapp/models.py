from django.db import models


# Create your models here.
class MainCategory(models.Model):
    maincategory_id = models.CharField(max_length=10, primary_key=True)
    maincategory_name = models.CharField(max_length=100)

    def generate_maincategory_id(self):
        pattern = "FGMC"
        main_pattern = Admin.objects.filter(maincategory_id__startswith=str(pattern))
        count = main_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.maincategory_id:
            self.maincategory_id = self.generate_maincategory_id()

        super().save(*args, **kwargs)
    class Meta:
        db_table = "maincategory_table"


class SubCategory(models.Model):
    subcategory_id = models.CharField(max_length=10, primary_key=True)
    subcategory_name = models.CharField(max_length=100)
    maincategory_id = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def generate_subcategory_id(self):
        pattern = "FGSC"
        sub_pattern = Admin.objects.filter(subcategory_id__startswith=str(pattern))
        count = sub_pattern.count() + 1
        return f"{pattern}-{count:03d}"

    def save(self, *args, **kwargs):
        if not self.subcategory_id:
            self.subcategory_id = self.generate_subcategory_id()

        super().save(*args, **kwargs)
    class Meta:
        db_table = "subcategory_table"
