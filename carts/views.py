from django.shortcuts import render, redirect
from .models import Cart, CartEntry
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home_page(request):
    entries = CartEntry.objects.entries(request)

    total = 0
    # for entry in entries:
    #     subtotal = entry.sku_product.master.costo * entry.quantity
    #     total += subtotal
    #
    if not entries:
        empty = True

    context = {
        "empty": empty,
        "entries": entries,
        "total": total,
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
