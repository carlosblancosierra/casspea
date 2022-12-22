from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('user-list', views.user_list_page, name="user-list"),
    # path('<str:username>', views.detail_page, name="detail"),
]
