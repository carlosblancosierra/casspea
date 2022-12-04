from django.shortcuts import render, redirect
from carts.models import Cart, CartEntry
from addresses.models import Address
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Order, STATUS_CHOICES


# from .emails import nueva_orden_mail_staff, nueva_orden_mail_client


# Create your views here.

@login_required
def address_page(request):
    if not request.user.is_authenticated:
        return redirect('/login?next=/orders/address')

    entries = CartEntry.objects.entries(request)
    if not entries.exists():
        return redirect("carts:home")

    user = request.user

    address_id = request.session.get("address_id", None)
    addresses = Address.objects.filter(user=user, active=True)
    address_qs = addresses.filter(id=address_id)
    address_to_update = None

    if len(address_qs) == 1:
        address_to_update = address_qs.first()
        addresses = addresses.exclude(id=address_id)

    context = {
        "addresses": addresses,
        "address": address_to_update,
    }

    form = request.POST
    if form:
        update_address_id = form.get('update_address_id', False)
        reuse_address_id = form.get('reuse_address_id', False)
        delete_address_id = form.get('delete_address_id', False)

        if update_address_id:
            address_qs = Address.objects.filter(id=address_id)
            full_name = form['full_name']
            street = form['street']
            postal_code = form['postal_code']
            city = form['city']
            tel = form['tel']
            country = form['country']
            address_qs_unique = len(address_qs) == 1

            all_variables = [address_qs_unique, full_name, street, postal_code, city, tel, country]

            if all(all_variables):
                address_qs.update(
                    full_name=full_name,
                    street=street,
                    postal_code=postal_code,
                    city=city,
                    tel=tel,
                    country=country,
                )

            request.session['address_id'] = form['update_address_id']
        elif reuse_address_id:
            request.session['address_id'] = reuse_address_id
        elif delete_address_id:
            Address.objects.filter(id=delete_address_id).update(active=False)
            return redirect('orders:address')
        else:
            full_name = form['full_name']
            street = form['street']
            postal_code = form['postal_code']
            city = form['city']
            tel = form['tel']
            country = form['country']

            address = Address(
                full_name=full_name,
                street=street,
                postal_code=postal_code,
                city=city,
                tel=tel,
                country=country,
                user=request.user
            )
            address.save()

            request.session['address_id'] = address.id

        return redirect('orders:confirm')

    return render(request, "orders/address.html", context)


@login_required
def confirm_page(request):
    cart_id = request.session.get("cart_id", None)
    address_id = request.session.get("address_id", None)
    entries = CartEntry.objects.filter(cart__id=cart_id)

    if not entries.exists():
        return redirect("carts:home")

    total = 0
    # for entry in entries:
        # subtotal = entry.sku_product.master.costo * entry.quantity
        # total += subtotal

    address = None
    address_qs = Address.objects.filter(id=address_id)
    if len(address_qs) == 1:
        address = address_qs.first()

    form = request.POST
    if form:
        order = Order(user=request.user, direccion_entrega=address)
        order.save()
        request.session['order_id'] = order.id

        for entry in entries:
            order.cart_entries.add(entry)

        request.session['cart_id'] = None
        request.session['address_id'] = None

        # nueva_orden_mail_staff(order)
        # nueva_orden_mail_client(order)
        return redirect('orders:created')

    context = {
        "address": address,
        "entries": entries,
        "total": total,
    }

    return render(request, "orders/confirm.html", context)


@login_required
def created_page(request):
    order = None
    order_id = request.session.get("order_id")
    order_qs = Order.objects.filter(id=order_id)
    if len(order_qs) == 1:
        order = order_qs.first()

    print(order)
    context = {
        "order": order,
    }

    return render(request, "orders/created.html", context)


@staff_member_required
def staff_list_page(request):
    order_qs = Order.objects.all()

    paginator = Paginator(order_qs, 50)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": page_obj,
    }

    return render(request, "orders/staff-list.html", context)


@staff_member_required
def staff_detail_page(request, order_id):
    order = None
    order_qs = Order.objects.filter(order_id=order_id)
    if len(order_qs) == 1:
        order = order_qs.first()

    if request.POST:
        form = request.POST
        status = form.get('order-status')
        if order:
            order.status = status
            order.save()
            messages.success(request, 'Estatus de orden actualizado')

    context = {
        "order": order,
        "address": order.direccion_entrega,
        "entries": order.cart_entries.all,
        "STATUS_CHOICES": STATUS_CHOICES,
    }

    return render(request, "orders/staff-detail.html", context)


@login_required
def detail_page(request, order_id):
    order = None
    order_qs = Order.objects.filter(order_id=order_id)

    if len(order_qs) == 1:
        order = order_qs.first()

    if order.user != request.user:
        return HttpResponseForbidden()

    context = {
        "order": order,
        "address": order.direccion_entrega,
        "entries": order.cart_entries.all,
    }

    return render(request, "orders/detail.html", context)


@login_required
def list_page(request):
    order_qs = Order.objects.filter(user=request.user)

    context = {
        "orders": order_qs,
    }

    return render(request, "orders/list.html", context)


@staff_member_required
def email_test(request):
    order_id = ""
    # nueva_orden_mail_staff("JM3")
    # print(nueva_orden_mail_client(order_id))

    qs = Order.objects.filter(order_id=order_id)
    context = {"order": qs.first()}

    return render(request, "mails/orders/asd-inline.html", context)
