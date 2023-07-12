from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_page, name="home"),
    path('box/add', views.add_box_to_cart, name="add_boxes"),
    path('box/remove', views.remove_box_from_cart, name="remove_boxes"),
    path('luxury-handmade-chocolates/box-<str:size>', views.box_page, name="boxes"),

]
