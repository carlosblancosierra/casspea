from django.urls import path

from . import views

app_name = 'flavours'

urlpatterns = [
    path('', views.home_page, name="home"),
]

api_urls = [
    path('', views.FlavourListView.as_view(), name='flavour-list'),
]
