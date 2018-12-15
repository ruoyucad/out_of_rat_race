import random
import os
from django.db import models

# Create your models here.


def g4et_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = g4et_filename_ext(filename)
    new_filename = random.randint(1, 393439353)
    final_filename = f'{new_filename}{ext}'
    return f"products/{new_filename}/{final_filename}"


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.99)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.title
