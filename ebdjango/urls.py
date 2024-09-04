from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from accounts.views import login_page, register_page_local
from leads.views import newsletter_subscribe, download_subscribers
from . import views
from flavours.urls import api_urls

urlpatterns = [
    path('', views.home_page, name='home'),
    path('contact-us', views.contact_us_page, name="contact"),
    path('privacy', views.privacy_page, name="privacy"),
    path('about-us', views.about_us_page, name="about"),
    path('fequently-asked-questions', views.faqs_page, name="faqs"),
    path('valentines-day', views.valentines_day_page, name="valentines"),
    path('custom-orders', views.custom_orders_landing_page, name="custom_orders"),

    path('newsletter_subscribe', newsletter_subscribe,
         name="subscribe_newsletter"),
    path('download_subscribers', download_subscribers,name="download_subscribers"),


    path('accounts/', include('accounts.urls')),
    path('accounts/', include('accounts.passwords.urls')),
    path('addresses/', include('addresses.urls')),
    path('cart/', include('carts.urls')),
    path('custom_chocolates/', include('custom_chocolates.urls')),
    path('discounts/', include('discounts.urls')),

    # path('custom_boxes/', include('custom_boxes.urls')),

    path('dashboard/', include('dashboards.urls')),
    path('orders/', include('orders.urls')),
    path('shop-now/', include('store.urls')),
    path('flavours/', include('flavours.urls')),

    path('logout', LogoutView.as_view(), name='logout'),
    path('login', login_page, name="login"),
    path('register', register_page_local, name="register"),

    path('send_test_email', views.send_test_email, name="mail_test"),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', views.SitemapView.as_view(content_type='application/xml'), name='sitemap'),

    path('admin/', admin.site.urls),

    path('api/flavours/', include(api_urls)),

]

if settings.STATIC_LOCAL:
    # test mode
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
