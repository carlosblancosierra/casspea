from django.urls import path

from . import views

app_name = 'address'

urlpatterns = [
    path('list', views.list_page, name="list"),
    path('<str:address_id>', views.detail_page, name="detail"),
]
