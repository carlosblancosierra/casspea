from django.urls import path

from . import views

app_name = 'custom_chocolates'

urlpatterns = [
    path('test', views.test_page, name="test"),
]
