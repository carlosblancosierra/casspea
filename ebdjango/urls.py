"""ebdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from accounts.views import login_page, register_page_local

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('contact-us', views.contact_us_page, name="contact"),
    path('about-us', views.about_us_page, name="about"),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('accounts.passwords.urls')),
    path('addresses/', include('addresses.urls')),
    path('cart/', include('carts.urls')),
    path('custom_chocolates/', include('custom_chocolates.urls')),
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
