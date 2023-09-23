from django.db import models


class ShippingTypeManager(models.Manager):
    def active(self):
        return self.model.objects.filter(active=True)


# Create your models here.
class ShippingType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    delivery_time = models.CharField(max_length=100)
    cost = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} ￡{} GBP".format(self.name, self.delivery_time, self.cost)

    objects = ShippingTypeManager()

    class Meta:
        ordering = ["-default", "cost"]

    def save(self, *args, **kwargs):
        if self.default:
            # If this instance is set as default, ensure all other instances are not default
            ShippingType.objects.exclude(pk=self.pk).update(default=False)
        super().save(*args, **kwargs)

    @property
    def cents(self):
        return int(self.cost * 100)
