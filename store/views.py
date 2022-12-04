from django.shortcuts import render, redirect

from flavours.models import PreBuildFlavour

from boxes.models import Box, BoxSize
from carts.models import CartEntry

from .models import FLAVOURS, FLAVOUR_FORMAT


# Create your views here.
def home_page(request):
    if request.POST:
        size = request.POST.get('size', None)
        if size:
            return redirect("store:boxes", size=size)

    context = {
    }

    return render(request, "store/home.html", context)


def box_page(request, size=None):
    prebuilds = PreBuildFlavour.objects.filter(active=True)

    context = {
        "size": size,
        "flavours": FLAVOURS,
        "prebuilds": prebuilds,
        "PRE_BUILT": Box.PRE_BUILT,
        "PICK_AND_MIX": Box.PICK_AND_MIX,
        "FLAVOUR_FORMAT": FLAVOUR_FORMAT,
    }

    return render(request, "store/box.html", context)


def add_box_to_cart(request):
    form = request.POST
    print(form)

    if form:
        # get box data
        size = form.get('size', None)
        flavour_format = form.get(FLAVOUR_FORMAT, None)
        print(flavour_format)
        pre_built = form.get(Box.PRE_BUILT, None)

        # Check if Size obj exists
        if not size:
            return redirect('store:home')
        size_qs = BoxSize.objects.filter(active=True, size=size)
        print(size_qs)

        if len(size_qs) is not 1:
            return redirect('store:home')
        size_obj = size_qs.first()

        # Check if Prebuilt obj exists
        if not pre_built:
            return redirect('store:home')
        pre_built_qs = PreBuildFlavour.objects.filter(active=True, slug=pre_built)
        print(pre_built_qs)

        if len(pre_built_qs) is not 1:
            return redirect('store:home')

        pre_built_obj = pre_built_qs.first()

        # create box
        new_box = Box(size=size_obj, flavour_format=flavour_format, pre_built=pre_built_obj)
        new_box.save()

        # create entry
        box_quantity = form.get('box_quantity', None)
        cart_entry = CartEntry.objects.new(request, product=new_box, quantity=box_quantity)
        print("cart_entry")
        print(cart_entry)

    context = {}
    return redirect('carts:home')
