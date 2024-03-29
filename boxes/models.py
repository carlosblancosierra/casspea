from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField

from flavours.models import Flavour, PreBuildFlavour, FlavourChoice
from custom_chocolates.models import UserChocolateDesign
from django.utils.text import slugify


# Create your models here.
def upload_location(instance, filename):
    return "box-size-img/%s/%s" % (instance.id, filename)


class BoxSizeManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class BoxSize(models.Model):
    size = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    price_id = models.CharField(max_length=200, null=True, blank=True)
    custom_price = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    custom_price_id = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    sold_out = models.BooleanField(default=False)
    custom_chocolates_min = models.PositiveIntegerField(blank=True, null=True, default=1)
    slug = models.SlugField(blank=True)
    special_box = models.BooleanField(default=False)
    valentines_box = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    prebuild_options = models.ManyToManyField(PreBuildFlavour, blank=True, related_name="prebuild_options")

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    store_image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                      processors=[ResizeToFill(1500, 1500)],
                                      format='JPEG',
                                      options={'quality': 100})

    image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                processors=[ResizeToFill(1500, 1500)],
                                format='JPEG',
                                options={'quality': 100})
    image2 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 1500)],
                                 format='JPEG',
                                 options={'quality': 100})
    image3 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 1500)],
                                 format='JPEG',
                                 options={'quality': 100})
    image4 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 1500)],
                                 format='JPEG',
                                 options={'quality': 100})
    image5 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 1500)],
                                 format='JPEG',
                                 options={'quality': 100})

    def __str__(self):
        return self.slug

    objects = BoxSizeManager()

    class Meta:
        ordering = ['size']

    def get_absolute_url(self):
        if self.special_box:
            return f"/shop-now/{self.slug}"
        else:
            return f"/shop-now/luxury-handmade-chocolates/{self.slug}"

        # return f"/shop-now/luxury-handmade-chocolates/box-{self.size}"


    def images(self):
        images = []

        if self.image:
            images.append(self.image)
        if self.image2:
            images.append(self.image2)
        if self.image3:
            images.append(self.image3)
        if self.image4:
            images.append(self.image4)
        if self.image5:
            images.append(self.image5)

        return images

    def save(self, *args, **kwargs):
        # Generate a slug from the title if one is not provided
        if not self.slug:
            self.slug = slugify("Box of {}".format(self.size))
        super().save(*args, **kwargs)


class Box(models.Model):
    PRE_BUILT = "pre_built"
    CUSTOM = "custom"
    PICK_AND_MIX = "pick_and_mix"

    FLAVOURS_FORMAT_CHOICES = (
        (CUSTOM, "Custom"),
        (PRE_BUILT, "Pre-Built"),
        (PICK_AND_MIX, "Pick and Mix"),
    )

    size = models.ForeignKey(BoxSize, on_delete=models.PROTECT, null=True)
    flavour_format = models.CharField(max_length=30, choices=FLAVOURS_FORMAT_CHOICES, default=PRE_BUILT)
    pre_built = models.ForeignKey(PreBuildFlavour, on_delete=models.PROTECT, null=True)
    selected_prebuilts = models.ManyToManyField(PreBuildFlavour, blank=True, related_name="selected_prebuilts")
    selected_flavours = models.ManyToManyField(FlavourChoice, blank=True, related_name="selected_flavours")

    custom_design = models.ForeignKey(UserChocolateDesign, blank=True, null=True, on_delete=models.PROTECT)
    custom_chocolates_flavours = models.ManyToManyField(Flavour, blank=True)

    # price_stripe_id = models.CharField(max_length=100, null=True, blank=True)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Box of {} Chocolates, {}".format(self.size, self.flavour_format)

    @property
    def image(self):
        return self.size.image

    @property
    def price(self):
        if self.custom_design:
            return self.size.custom_price
        else:
            return self.size.price

    @property
    def flavours(self):
        if self.flavour_format == Box.PRE_BUILT:
            return self.selected_prebuilts
        elif self.selected_flavours.exists():
            return self.selected_flavours
        elif self.custom_chocolates_flavours.exists():
            return self.custom_chocolates_flavours

    @property
    def get_price_id(self):
        if self.custom_design:
            return self.size.custom_price_id
        else:
            return self.size.price_id

    @property
    def name(self):
        return self.size.name

    @property
    def sold_out(self):
        return self.size.sold_out
