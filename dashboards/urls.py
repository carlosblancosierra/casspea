from django.urls import path

from . import views

app_name = 'dashboards'

urlpatterns = [
    path('client', views.client_page, name="client"),
    path('staff', views.staff_page, name="staff"),
    path('week_orders', views.week_orders_page, name="week_orders"),
    path('date', views.date_orders_page, name="date"),
]
