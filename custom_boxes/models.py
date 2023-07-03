from django.db import models

from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

User = settings.AUTH_USER_MODEL


# Create your models here.

def upload_location(instance, filename):
    return "custom-boxes/logos/%s/%s" % (instance.id, filename)


class CustomBoxLogo(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                processors=[ResizeToFill(2000, 2000)],
                                format='PNG',
                                options={'quality': 97})

    def __str__(self):
        return self.image.url
