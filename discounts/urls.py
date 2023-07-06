from django.urls import path
from . import views

app_name = 'discounts'

urlpatterns = [
    path('validate/', views.validate_discount, name='validate_discount'),
]
