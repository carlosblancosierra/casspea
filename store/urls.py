from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_page, name="home"),
    path('box/add', views.add_box_to_cart, name="add_boxes"),
    path('box/<str:size>/pieces', views.box_page, name="boxes"),

]
