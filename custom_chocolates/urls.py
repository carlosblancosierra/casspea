from django.urls import path

from . import views

app_name = 'custom_chocolates'

urlpatterns = [
    # path('test', views.test_page, name="test"),
    path('', views.home_page, name="home"),
    path('box_size', views.box_size_page, name="box_size"),
    path('box_size/<str:size>', views.add_to_cart_page, name="q"),
    path('design/<str:slug>', views.design_page, name="design_page"),
    path('add_boxes', views.add_box_to_cart, name="add_boxes"),
    # path('lot/add', views.add_lot_to_cart, name="add_lots"),
    path('lot/add', views.add_lot_to_cart, name="add_lot"),
    path('lot/<str:size>', views.lot_page, name="lots"),
]
