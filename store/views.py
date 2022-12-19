from django.shortcuts import render, redirect

from flavours.models import PreBuildFlavour, Flavour, FlavourChoice

from boxes.models import Box, BoxSize
from carts.models import CartEntry
from lots.models import Lot, LotSize

from .models import FLAVOURS, FLAVOUR_FORMAT


# Create your views here.
def home_page(request):
    qs = BoxSize.objects.active()

    context = {
        "title": "PICK YOUR BOX",
        "qs": qs,
    }

    return render(request, "store/home.html", context)


def box_page(request, size=None):
    prebuilds = PreBuildFlavour.objects.filter(active=True)
    flavours = Flavour.objects.active()
    box_size_qs = BoxSize.objects.filter(size=size)

    box_obj = None
    if len(box_size_qs) == 1:
        box_obj = box_size_qs.first()

    context = {
        "size": size,
        "flavours": flavours,
        "prebuilds": prebuilds,
        "PRE_BUILT": Box.PRE_BUILT,
        "PICK_AND_MIX": Box.PICK_AND_MIX,
        "FLAVOUR_FORMAT": FLAVOUR_FORMAT,
        "title": "BOXES",
        "box_obj": box_obj,
    }

    return render(request, "store/box.html", context)


def add_box_to_cart(request):
    form = request.POST
    # print(form)

    if form:
        # get box data
        size = form.get('size', None)
        flavour_format = form.get(FLAVOUR_FORMAT, None)

        # Check if Size obj exists
        if not size:
            return redirect('store:home')
        size_qs = BoxSize.objects.filter(active=True, size=size)

        if len(size_qs) != 1:
            return redirect('store:home')
        size_obj = size_qs.first()

        if flavour_format == Box.PRE_BUILT:
            selected_prebuilts = []
            prebuilds = PreBuildFlavour.objects.filter(active=True)
            for obj in prebuilds:
                selected = form.get(obj.slug, None)
                if selected:
                    selected_prebuilts.append(obj)

            # create box
            new_box = Box(size=size_obj, flavour_format=flavour_format)
            new_box.save()
            new_box.selected_prebuilts.set(selected_prebuilts)

        elif flavour_format == Box.PICK_AND_MIX:
            flavours = Flavour.objects.active()
            selected_flavours = []
            for obj in flavours:
                quantity = form.get(obj.slug, 0)
                # print(obj.slug, quantity)

                if int(quantity) > 0:
                    flavour_choice_obj = FlavourChoice(quantity=quantity, flavour=obj)
                    flavour_choice_obj.save()
                    selected_flavours.append(flavour_choice_obj)

            # print(selected_flavours)

            new_box = Box(size=size_obj, flavour_format=flavour_format)
            new_box.save()
            new_box.selected_flavours.set(selected_flavours)
        else:
            return redirect('store:home')

        # create entry
        box_quantity = form.get('box_quantity', None)
        cart_entry = CartEntry.objects.new(request, product=new_box, quantity=box_quantity)
        # print("cart_entry")
        # print(cart_entry)

    return redirect('carts:home')


def lot_page(request, size=None):
    prebuilds = PreBuildFlavour.objects.filter(active=True)
    flavours = Flavour.objects.active()
    lot_size_qs = LotSize.objects.filter(size=size)

    obj = None
    if len(lot_size_qs) == 1:
        obj = lot_size_qs.first()

    context = {
        "size": size,
        "flavours": flavours,
        "prebuilds": prebuilds,
        "PRE_BUILT": Lot.PRE_BUILT,
        "PICK_AND_MIX": Lot.PICK_AND_MIX,
        "FLAVOUR_FORMAT": FLAVOUR_FORMAT,
        "title": "LOTS",
        "obj": obj,
    }

    return render(request, "store/lot.html", context)


def add_lot_to_cart(request):
    form = request.POST
    print(form)

    if form:
        # get box data
        size = form.get('size', None)
        flavour_format = form.get(FLAVOUR_FORMAT, None)

        # Check if Size obj exists
        if not size:
            return redirect('store:home')
            print("error 144")
        size_qs = LotSize.objects.filter(active=True, size=size)

        if len(size_qs) != 1:
            return redirect('store:home')
            print("error 148")
        size_obj = size_qs.first()

        if flavour_format == Lot.PRE_BUILT:
            selected_prebuilts = []
            prebuilds = PreBuildFlavour.objects.filter(active=True)
            for obj in prebuilds:
                selected = form.get(obj.slug, None)
                if selected:
                    selected_prebuilts.append(obj)

            # create box
            new_lot = Lot(size=size_obj, flavour_format=flavour_format)
            new_lot.save()
            new_lot.selected_prebuilts.set(selected_prebuilts)

        elif flavour_format == Lot.PICK_AND_MIX:
            flavours = Flavour.objects.active()
            selected_flavours = []
            for obj in flavours:
                quantity = form.get(obj.slug, 0)
                print(obj.slug, quantity)

                if int(quantity) > 0:
                    flavour_choice_obj = FlavourChoice(quantity=quantity, flavour=obj)
                    flavour_choice_obj.save()
                    selected_flavours.append(flavour_choice_obj)

            print(selected_flavours)

            new_lot = Lot(size=size_obj, flavour_format=flavour_format)
            new_lot.save()
            new_lot.selected_flavours.set(selected_flavours)
        else:
            return redirect('store:home')

        # create entry
        cart_entry = CartEntry.objects.new(request, product=new_lot, quantity=1)
        print("cart_entry")
        print(cart_entry)

    return redirect('carts:home')


def remove_box_from_cart(request):
    form = request.POST

    if form:
        obj_id = form.get('obj_id', None)
        CartEntry.objects.set_inactive(request, id=obj_id)

    return redirect('carts:home')
