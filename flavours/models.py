from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


# Create your models here.

class AllergenManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Allergen(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    objects = AllergenManager()


def upload_location(instance, filename):
    return "flavour-img/%s/%s" % (instance.id, filename)


class FlavourManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Flavour(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    description = models.TextField(blank=True, null=True)

    allergens = models.ManyToManyField(Allergen, blank=True)

    image = ProcessedImageField(upload_to=upload_location, null=True, blank=True,
                                processors=[ResizeToFill(1500, 998)],
                                format='JPEG',
                                options={'quality': 95})

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    objects = FlavourManager()

    @property
    def allergens_str(self):
        text = ""
        if len(self.allergens.all()) > 0:
            for obj in self.allergens.all():
                text = text + obj.name + " "
        return text



class FlavourChoice(models.Model):
    flavour = models.ForeignKey(Flavour, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} of {}".format(self.quantity, self.flavour)


class PreBuildFlavour(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def create_flavor_slug(instance, new_slug=None):
    slug = slugify(instance.name)

    if new_slug is not None:
        slug = new_slug

    qs = Flavour.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance=slug, new_slug=new_slug)

    return slug


def pre_save_flavor_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_flavor_slug(instance)


pre_save.connect(pre_save_flavor_receiver, sender=Flavour)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)

    if new_slug is not None:
        slug = new_slug

    qs = PreBuildFlavour.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance=slug, new_slug=new_slug)

    return slug


def pre_save_pre_build_flavor_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_pre_build_flavor_receiver, sender=PreBuildFlavour)


def create_alergen_slug(instance, new_slug=None):
    slug = slugify(instance.name)

    if new_slug is not None:
        slug = new_slug

    qs = Allergen.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance=slug, new_slug=new_slug)
    return slug


def pre_save_allergen_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_alergen_slug(instance)


pre_save.connect(pre_save_allergen_receiver, sender=Allergen)
