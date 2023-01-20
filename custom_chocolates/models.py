from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
import json
User = settings.AUTH_USER_MODEL


# Create your models here.
def upload_location(instance, filename):
    return "chocolate-design-layer-img/%s/%s" % (instance.id, filename)


class ChocolateDesignLayer(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    top_image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                    processors=[ResizeToFill(2000, 2000)],
                                    format='PNG',
                                    options={'quality': 95})
    side_image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                     processors=[ResizeToFill(2000, 2000)],
                                     format='PNG',
                                     options={'quality': 95})
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    @property
    def images(self):
        if self.top_image and self.side_image:
            images = {
                "id": self.id,
                "top": self.top_image.url,
                "side": self.side_image.url
            }
            return json.dumps(images)


class ChocolateDesign(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    background_options = models.ManyToManyField(ChocolateDesignLayer, related_name="background_options", blank=True)
    layer1_options = models.ManyToManyField(ChocolateDesignLayer, related_name="layer1_options", blank=True)
    layer2_options = models.ManyToManyField(ChocolateDesignLayer, related_name="layer2_options", blank=True)
    layer3_options = models.ManyToManyField(ChocolateDesignLayer, related_name="layer3_options", blank=True)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)


class UserChocolateDesign(models.Model):
    design = models.ForeignKey(ChocolateDesign, related_name="design", on_delete=models.PROTECT)
    background = models.ForeignKey(ChocolateDesignLayer, related_name="background",
                                   on_delete=models.PROTECT)
    layer1 = models.ForeignKey(ChocolateDesignLayer, related_name="layer1", on_delete=models.PROTECT)
    layer2 = models.ForeignKey(ChocolateDesignLayer, related_name="layer2", on_delete=models.PROTECT)
    layer3 = models.ForeignKey(ChocolateDesignLayer, related_name="layer3", on_delete=models.PROTECT)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.design)
