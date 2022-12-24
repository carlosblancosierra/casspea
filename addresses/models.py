from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class Address(models.Model):
    full_name = models.CharField(max_length=500)
    street = models.CharField(max_length=500)
    postal_code = models.CharField(max_length=120)
    city = models.CharField(max_length=500)
    tel = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, default="Mexico")
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return f"/addresses/{self.id}"
