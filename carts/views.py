from django.shortcuts import render, redirect
from .models import Cart, CartEntry
from django.contrib.auth.decorators import login_required


# Create your views here.
def home_page(request):
    entries = CartEntry.objects.entries(request)
    empty = CartEntry.objects.empty_cart(request)
    gift_message = request.session.get('gift_message', None)
    shipping_date = request.session.get("shipping_date", None)

    subtotal = CartEntry.objects.cart_subtotal(request)
    total = CartEntry.objects.cart_total(request)
    shipping_cost = 5.99
    shipping_free = CartEntry.objects.shipping_free(request)
    if shipping_free:
        shipping_cost = 0

    if request.POST:
        gift_message = request.POST.get('gift_message', None)
        request.session['gift_message'] = gift_message

        shipping_date = request.POST.get('shipping_date', None)
        request.session['shipping_date'] = shipping_date

        return redirect('orders:address')

    context = {
        "title": "Cart",
        "empty": empty,
        "entries": entries,
        "total": total,
        "gift_message": gift_message,
        "shipping_date": shipping_date,
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "shipping_free": shipping_free,

    }

    return render(request, "carts/home.html", context)


@login_required
def agregar_page(request):
    form = request.POST
    if form:
        for sku_product, quantity in form.items():
            if sku_product == "csrfmiddlewaretoken":
                continue
            CartEntry.objects.new_or_update(request, sku_product, quantity)

    return redirect("carts:home")


@login_required
def delete_entry_page(request):
    form = request.POST
    if form:
        sku_product = form['delete-entry-sku']
        CartEntry.objects.new_or_update(request, sku_product, 0)

    return redirect("carts:home")


@login_required
def add_1_page(request):
    if request.POST:
        data = request.POST.dict()
        sku_product_sku = data["sku_product_sku"]

        CartEntry.objects.add_1(request, sku_product_sku)
        return redirect("carts:home")


@login_required
def remove_1_page(request):
    if request.POST:
        data = request.POST.dict()
        sku_product_sku = data["sku_product_sku"]

        CartEntry.objects.remove_1(request, sku_product_sku)
        return redirect("carts:home")
