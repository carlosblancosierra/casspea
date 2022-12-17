from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.

class FlavourManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Flavour(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    objects = FlavourManager()


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
