from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from orders.models import Order
from django.contrib.admin.views.decorators import staff_member_required

from carts.models import Cart, CartEntry

from django.contrib.auth import get_user_model

# Create your views here.

@login_required
def client_page(request):
    user = request.user

    if request.user.is_staff:
        return redirect('dashboards:staff')

    orders_qs = Order.objects.filter(user=user)

    context = {
        "orders": orders_qs[:5],
        "total_orders": len(orders_qs),
    }

    return render(request, "dashboards/client.html", context)


@staff_member_required
def staff_page(request):
    orders_qs = Order.objects.all()
    User = get_user_model()
    users = User.objects.all()

    context = {
        "orders": orders_qs[:10],
        "users": users[:10],
    }

    return render(request, "dashboards/staff.html", context)
