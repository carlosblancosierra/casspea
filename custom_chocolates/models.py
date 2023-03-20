from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.conf import settings
import json

User = settings.AUTH_USER_MODEL


# Create your models here.
class LayerColor(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['title']


class ChocolateDesignLayerType(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['title']


def upload_location(instance, filename):
    return "chocolate-design-layer-img/%s/%s" % (instance.id, filename)


class ChocolateDesignLayer(models.Model):
    type = models.ForeignKey(ChocolateDesignLayerType, related_name="type", on_delete=models.PROTECT, null=True,
                             blank=True)
    color = models.ForeignKey(LayerColor, related_name="color", on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=120, blank=True, null=True)
    top_image = ProcessedImageField(upload_to=upload_location,
                                    null=True, blank=True,
                                    format='PNG')
    side_image = ProcessedImageField(upload_to=upload_location,
                                     null=True, blank=True,
                                     format='PNG')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.type, self.color)

    @property
    def images(self):
        if self.top_image and self.side_image:
            images = {
                "id": self.id,
                "top": self.top_image.url,
                "side": self.side_image.url
            }
            return json.dumps(images)

    class Meta:
        ordering = ['type', 'color']


class ChocolateDesignBase(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    base_color = models.ForeignKey(LayerColor, related_name="base_color", on_delete=models.PROTECT, null=True,
                                   blank=True)
    top_image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                    # processors=[ResizeToFill(1000, 1000)],
                                    format='JPEG',
                                    options={'quality': 90})
    side_image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                     # processors=[ResizeToFill(1000, 1000)],
                                     format='JPEG',
                                     options={'quality': 90})
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.base_color)

    @property
    def images(self):
        if self.top_image and self.side_image:
            images = {
                "id": self.id,
                "top": self.top_image.url,
                "side": self.side_image.url
            }
            return json.dumps(images)

    class Meta:
        ordering = ['base_color']


class ChocolateDesign(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    # background_options = models.ManyToManyField(ChocolateDesignLayer, related_name="background_options", blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    base_options = models.ManyToManyField(ChocolateDesignBase, related_name="base_options", blank=True)
    layer1_name = models.CharField(max_length=120, blank=True, null=True)
    layer1_options = models.ManyToManyField(ChocolateDesignLayer, related_name="layer1_options", blank=True)
    layer2_active = models.BooleanField(default=False)
    layer2_name = models.CharField(max_length=120, blank=True, null=True)
    layer2_options = models.ManyToManyField(ChocolateDesignLayer, related_name="layer2_options", blank=True)
    layer3_active = models.BooleanField(default=False)
    layer3_name = models.CharField(max_length=120, blank=True, null=True)
    layer3_options = models.ManyToManyField(ChocolateDesignLayer, related_name="layer3_options", blank=True)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return f"/custom_chocolates/design/{self.slug}"

    class Meta:
        ordering = ['title']

    @property
    def featured_design(self):
        featured_designs = UserChocolateDesign.objects.filter(active=True, featured=True, design=self)
        if featured_designs.exists():
            return featured_designs.first()


class UserChocolateDesign(models.Model):
    design = models.ForeignKey(ChocolateDesign, related_name="design", on_delete=models.PROTECT)
    base = models.ForeignKey(ChocolateDesignBase, related_name="base",
                             on_delete=models.PROTECT, null=True)
    layer1 = models.ForeignKey(ChocolateDesignLayer, related_name="layer1", on_delete=models.PROTECT)
    layer2 = models.ForeignKey(ChocolateDesignLayer, related_name="layer2", on_delete=models.PROTECT, blank=True,
                               null=True)
    layer3 = models.ForeignKey(ChocolateDesignLayer, related_name="layer3", on_delete=models.PROTECT, blank=True,
                               null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.design.title

    class Meta:
        ordering = ['-timestamp']

    @property
    def description(self):
        return "Design: {}, Background: {}, {}: {}".format(
            self.design.title,
            self.base.title,
            self.design.layer1_name,
            self.layer1.title
        )


def create_chocolate_design_slug(instance, new_slug=None):
    slug = slugify(instance.title)

    if new_slug is not None:
        slug = new_slug

    qs = ChocolateDesign.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_chocolate_design_slug(instance=slug, new_slug=new_slug)
    return slug


def pre_save_allergen_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_chocolate_design_slug(instance)


pre_save.connect(pre_save_allergen_receiver, sender=ChocolateDesign)
