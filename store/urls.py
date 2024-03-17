from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_page, name="home"),
    path('snacks/<str:slug>', views.snacks_page, name="snacks_page"),
    path('box/add', views.add_box_to_cart, name="add_boxes"),
    path('product/add', views.add_product_to_cart, name="add_product"),
    path('box/add_special', views.add_special_box_to_cart, name="add_boxes_special"),
    path('box/remove', views.remove_box_from_cart, name="remove_boxes"),
    path('luxury-handmade-chocolates/<str:slug>', views.box_page, name="boxes"),
    path('<str:slug>', views.valentines_box_page, name="boxes-valentines"),
]
