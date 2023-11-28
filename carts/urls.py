from django.urls import path

from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.home_page_v2, name="home"),
    path('agregar', views.agregar_page, name="add"),
    path('borrar', views.delete_entry_page, name="delete_entry"),
    path('add_1', views.add_1_page, name="add_1"),
    path('remove_1', views.remove_1_page, name="remove_1"),
    path('old', views.home_page),

]
