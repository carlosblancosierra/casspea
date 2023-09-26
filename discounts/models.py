from django.db import models
from boxes.models import BoxSize


# Create your models here.
class Discount(models.Model):
    PERCENTAGE = "Percentage"
    FIXED_AMOUNT = "Fixed Amount"
    CHOICES = [
        (PERCENTAGE, PERCENTAGE),
        (FIXED_AMOUNT, FIXED_AMOUNT),
    ]

    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    stripe_id = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=CHOICES, default=PERCENTAGE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_uses = models.PositiveIntegerField(default=1)  # New field for maximum number of uses
    box_exclusions = models.ManyToManyField(BoxSize, related_name="box_exclusions", blank=True)

    def __str__(self):
        return self.title
