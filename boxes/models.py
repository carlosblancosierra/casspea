from django.db import models

from flavours.models import PreBuildFlavour


# Create your models here.


class BoxSize(models.Model):
    size = models.PositiveIntegerField()

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Box of {} pieces".format(self.size)


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
    # flavours = models.ManyToManyField(FlavourEntrySelection)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.size, self.flavour_format)
