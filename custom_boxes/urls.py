from django.urls import path

from . import views

app_name = 'custom_boxes'

urlpatterns = [
    path('test', views.test_page, name="test"),
    path('preview/<str:logo_id>', views.box_preview_page, name="box-preview"),

]
