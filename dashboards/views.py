from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from orders.models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate

from carts.models import Cart, CartEntry

from django.contrib.auth import get_user_model


# Create your views here.

@login_required
def client_page(request):
    user = request.user

    if request.user.is_staff:
        return redirect('dashboards:week_orders')

    orders_qs = Order.objects.filter(user=user)

    context = {
        "orders": orders_qs[:5],
        "total_orders": len(orders_qs),
    }

    return render(request, "dashboards/client.html", context)


@staff_member_required
def staff_page(request):
    orders_qs = Order.objects.filter(payment_status="paid")
    User = get_user_model()
    users = User.objects.all()

    context = {
        "orders": orders_qs[:10],
        "users": users[:10],
    }

    return render(request, "dashboards/staff.html", context)


@staff_member_required
def week_orders_page(request):
    orders_qs = Order.objects.filter(payment_status="paid")

    today = datetime.now()
    week_offset = int(request.GET.get('week_offset', 1))

    start_date = today - timedelta(days=(7 * week_offset))

    date_range = [start_date - timedelta(days=i) for i in range(7)]

    recent_orders_by_day = {}

    for date in date_range:
        day_orders = orders_qs.filter(updated__date=date.date())
        day = {
            "orders": list(day_orders),
            "day_of_week": date.strftime('%A'),  # Add the day of the week
            "order_count": len(day_orders)
        }
        recent_orders_by_day[date.date()] = day

    context = {
        "recent_orders_by_day": recent_orders_by_day,
        "current_week_offset": week_offset,
    }

    return render(request, "dashboards/calendar.html", context)
