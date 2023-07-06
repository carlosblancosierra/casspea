from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from accounts.views import login_page, register_page_local
from leads.views import newsletter_subscribe
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('contact-us', views.contact_us_page, name="contact"),
    path('privacy', views.privacy_page, name="privacy"),
    path('about-us', views.about_us_page, name="about"),
    path('fequently-asked-questions', views.faqs_page, name="faqs"),
    path('emailtest', views.email_test_page),

    path('newsletter_subscribe', newsletter_subscribe, name="subscribe_newsletter"),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('accounts.passwords.urls')),
    path('addresses/', include('addresses.urls')),
    path('cart/', include('carts.urls')),
    path('custom_chocolates/', include('custom_chocolates.urls')),
    path('discounts/', include('discounts.urls')),

    # path('custom_boxes/', include('custom_boxes.urls')),

    path('dashboard/', include('dashboards.urls')),
    path('orders/', include('orders.urls')),
    path('store/', include('store.urls')),
    path('flavours/', include('flavours.urls')),

    path('logout', LogoutView.as_view(), name='logout'),
    path('login', login_page, name="login"),
    path('register', register_page_local, name="register"),

    path('admin/', admin.site.urls),

]

if settings.STATIC_LOCAL:
    # test mode
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
