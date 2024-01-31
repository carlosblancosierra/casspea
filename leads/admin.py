from django.contrib import admin
from .models import ContactMessage, NewsletterSubscriber

# Register your models here.
admin.site.register(ContactMessage)

@admin.register(NewsletterSubscriber)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    list_filter = ['subscribed_at']
    search_fields = ['subscribed_at',]
