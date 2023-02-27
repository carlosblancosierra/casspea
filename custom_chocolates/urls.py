from django.urls import path

from . import views

app_name = 'custom_chocolates'

urlpatterns = [
    path('test', views.test_page, name="test"),
    path('box_size', views.box_size_page, name="box_size"),
    path('box_size/<str:size>', views.add_to_cart_page, name="add_to_cart"),
    path('design/<str:slug>', views.design_page, name="design_page"),

]
