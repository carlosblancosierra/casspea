from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_page, name="home"),
    path('box/add', views.add_box_to_cart, name="add_boxes"),
    path('box/remove', views.remove_box_from_cart, name="remove_boxes"),
    # path('lot/add', views.add_lot_to_cart, name="add_lots"),
    path('box/<str:size>', views.box_page, name="boxes"),
    # path('lot/<str:size>', views.lot_page, name="lots"),

]
