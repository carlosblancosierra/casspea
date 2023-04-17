from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from flavours.models import PreBuildFlavour, FlavourChoice
from custom_chocolates.models import UserChocolateDesign
from decimal import Decimal


# Create your models here.
def upload_location(instance, filename):
    return "box-size-img/%s/%s" % (instance.id, filename)


class LotSizeManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class LotSize(models.Model):
    size = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    price_id = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    active = models.BooleanField(default=True)

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                processors=[ResizeToFill(1500, 998)],
                                format='JPEG',
                                options={'quality': 95})
    image2 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 998)],
                                 format='JPEG',
                                 options={'quality': 95})
    image3 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 998)],
                                 format='JPEG',
                                 options={'quality': 95})
    image4 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 998)],
                                 format='JPEG',
                                 options={'quality': 95})
    image5 = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                 processors=[ResizeToFill(1500, 998)],
                                 format='JPEG',
                                 options={'quality': 95})

    def __str__(self):
        return "Lot of {}".format(self.size)

    objects = LotSizeManager()

    def get_absolute_url(self):
        return f"/store/lot/{self.size}"


class LotPriceIds(models.Model):
    title = models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    limit = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.title


class Lot(models.Model):
    PRE_BUILT = "pre_built"
    CUSTOM = "custom"
    PICK_AND_MIX = "pick_and_mix"

    FLAVOURS_FORMAT_CHOICES = (
        (CUSTOM, "Custom"),
        (PRE_BUILT, "Pre-Built"),
        (PICK_AND_MIX, "Pick and Mix"),
    )

    prebuilt_size = models.PositiveIntegerField(blank=True, null=True)
    flavour_format = models.CharField(max_length=30, choices=FLAVOURS_FORMAT_CHOICES, default=PRE_BUILT)
    # pre_built = models.ForeignKey(PreBuildFlavour, on_delete=models.PROTECT, null=True)
    selected_prebuilts = models.ManyToManyField(PreBuildFlavour, blank=True, related_name="lot_selected_prebuilts")
    selected_flavours = models.ManyToManyField(FlavourChoice, blank=True, related_name="lot_selected_flavours")

    custom_design = models.ForeignKey(UserChocolateDesign, blank=True, null=True, on_delete=models.PROTECT)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Lot of {} Custom Chocolates".format(self.quantity, self.flavour_format)

    @property
    def price(self):
        price = 0.00

        if self.quantity < 100:
            price = 1.2
        elif self.quantity < 300:
            price = 1
        elif self.quantity < 500:
            price = 0.8
        else:
            price = 0.75

        return Decimal(price)

    @property
    def flavours(self):
        if self.flavour_format == Lot.PRE_BUILT:
            return self.selected_prebuilts
        elif self.selected_flavours.exists():
            return self.selected_flavours
        elif self.custom_chocolates_flavours.exists():
            return self.custom_chocolates_flavours

    @property
    def quantity(self):
        size = 0
        if self.flavour_format == Lot.PRE_BUILT:
            size = self.prebuilt_size
        elif self.flavour_format == Lot.PICK_AND_MIX:
            for flavour in self.selected_flavours.all():
                size += flavour.quantity
        return size

    @property
    def get_price_id(self):
        ids = LotPriceIds.objects.all()
        if self.quantity < 100:
            qs = ids.filter(limit=100)
        elif self.quantity < 300:
            qs = ids.filter(limit=300)
        elif self.quantity < 500:
            qs = ids.filter(limit=500)
        else:
            qs = ids.filter(limit=10000)

        if len(qs) == 1:
            obj = qs.first()
            return obj.stripe_id
