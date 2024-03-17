from django.db import models
from django.utils.text import slugify


type_choices = [
    ('general', 'General'),
    ('snacks', 'Snacks'),
]


def upload_location(instance, filename):
    return "product-img/%s/%s" % (instance.id, filename)


class ProductManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Product(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    weight = models.PositiveIntegerField(blank=True, null=True)

    color = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True)
    price_id = models.CharField(max_length=200, null=True, blank=True)

    custom_price = models.DecimalField(
        decimal_places=2, max_digits=20, blank=True, null=True)
    custom_price_id = models.CharField(max_length=200, null=True, blank=True)

    active = models.BooleanField(default=True)
    sold_out = models.BooleanField(default=False)

    slug = models.SlugField(blank=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)

    store_image = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    image2 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image3 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image4 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)
    image5 = models.ImageField(
        upload_to=upload_location, null=True, blank=True)

    type = models.CharField(max_length=20, choices=type_choices)

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        if not self.type == 'general':
            return f"/shop-now/{self.type}/{self.slug}"
        return f"/shop-now/{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
