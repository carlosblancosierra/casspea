from django.contrib import admin
from .models import ContactMessage, NewsletterSubscriber

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(NewsletterSubscriber)
