from django.shortcuts import render, redirect
from .models import Cart, CartEntry
from django.contrib.auth.decorators import login_required


# Create your views here.
def home_page(request):
    entries = CartEntry.objects.entries(request)
    empty = CartEntry.objects.empty_cart(request)
    cart, created = Cart.objects.new_or_get(request)
    discount = cart.discount
    discount_total = CartEntry.objects.discount_total(request)
    gift_message = request.session.get('gift_message', None)
    shipping_date = request.session.get("shipping_date", None)
    discount_error = request.session.get("discount_error", None)
    request.session['discount_error'] = None
    custom_chocolates = False
    for entry in entries:
        if custom_chocolates is False:
            if entry.product.custom_design:
                custom_chocolates = True

    total = cart.total
    subtotal = cart.subtotal
    shipping_free = cart.shipping_free

    amount_to_free_shipping = 0
    if not shipping_free:
        amount_to_free_shipping = int(45) - int(subtotal)

    if request.POST:
        gift_message = request.POST.get('gift_message', None)
        request.session['gift_message'] = gift_message

        shipping_date = request.POST.get('shipping_date', None)
        request.session['shipping_date'] = shipping_date

        return redirect('orders:guess_checkout')

    context = {
        "title": "Cart",
        "discount": discount,
        "discount_total": discount_total,
        "empty": empty,
        "entries": entries,
        "total": total,
        "gift_message": gift_message,
        "shipping_date": shipping_date,
        "subtotal": subtotal,
        # "shipping_cost": shipping_cost,
        "shipping_free": shipping_free,
        "discount_error": discount_error,
        "custom_chocolates": custom_chocolates,
        "amount_to_free_shipping": amount_to_free_shipping,
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
