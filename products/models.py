import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from .utils import unique_slug_generator

# Create your models here.


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    new_filename = random.randint(1, 393439353)
    final_filename = f'{new_filename}{ext}'
    return f"products/{new_filename}/{final_filename}"


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self,query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query)|
                   Q(price__icontains=query))
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().active().search(query)

class Product(models.Model):
    title         = models.CharField(max_length=120)
    slug          = models.SlugField(blank=True, unique=True)
    description   = models.TextField()
    price         = models.DecimalField(max_digits=10, decimal_places=2, default=0.99)
    image         = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured      = models.BooleanField(default=False)
    active        = models.BooleanField(default=True)
    timestamp     = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return f"/products/{self.slug}"
        return reverse('products:detail', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
