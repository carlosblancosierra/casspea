from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('email-test', views.email_test),
    path('address', views.address_page, name="address"),
    path('confirmar', views.confirm_page, name="confirm"),
    path('created', views.created_page, name="created"),
    path('staff-list', views.staff_list_page, name="staff-list"),
    path('list', views.list_page, name="list"),
    path('staff/<str:order_id>', views.staff_detail_page, name="staff-detail"),
    path('<str:order_id>', views.detail_page, name="detail"),
]
