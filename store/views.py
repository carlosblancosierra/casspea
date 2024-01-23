from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from flavours.models import PreBuildFlavour, Flavour, FlavourChoice
from boxes.models import Box, BoxSize
from carts.models import CartEntry
from lots.models import Lot, LotSize
from custom_chocolates.models import UserChocolateDesign
from .models import FLAVOURS, FLAVOUR_FORMAT


# Create your views here.
def home_page(request):
    qs = BoxSize.objects.filter(active=True, special_box=False)

    valentines_active = False
    valentines_boxes_qs = None

    context = {
        "title": "Build your box of CassPea chocolates.",
        "subtitle": "Let us surprise you with our own selection, or choose your own flavours with our Pick and Mix option!",
        "qs": qs,
        "valentines_active": valentines_active,
    }

    if valentines_active:
        valentines_boxes_qs = BoxSize.objects.filter(active=True, valentines_box=True)
        context["valentines_boxes_qs"] = valentines_boxes_qs

    return render(request, "store/home.html", context)


def box_page(request, slug=None):
    flavours = Flavour.objects.active()

    box_obj = get_object_or_404(BoxSize, slug=slug, special_box=False)

    context = {
        "size": box_obj.size,
        "flavours": flavours,
        "prebuilds": box_obj.prebuild_options.all(),
        "PRE_BUILT": Box.PRE_BUILT,
        "PICK_AND_MIX": Box.PICK_AND_MIX,
        "FLAVOUR_FORMAT": FLAVOUR_FORMAT,
        "title": box_obj.title,
        "box_obj": box_obj,
    }

    return render(request, "store/box.html", context)


def advent_calendar_page(request):
    prebuilds = PreBuildFlavour.objects.filter(active=True)
    box_size_qs = BoxSize.objects.filter(slug="Advent-Calendar")

    box_obj = None
    if len(box_size_qs) == 1:
        box_obj = box_size_qs.first()

    flavours_qs = Flavour.objects.active()

    context = {
        "size": box_obj.size,
        "prebuilds": prebuilds,
        "PRE_BUILT": Box.PRE_BUILT,
        "FLAVOUR_FORMAT": FLAVOUR_FORMAT,
        "title": box_obj.title,
        "box_obj": box_obj,
        "flavours_qs": flavours_qs
    }

    return render(request, "store/advent-calendar.html", context)


def valentines_box_page(request, slug=None):
    box_obj = get_object_or_404(BoxSize, slug=slug, special_box=True)
    flavours = Flavour.objects.active()

    context = {
        "size": box_obj.size,
        "flavours": flavours,
        "PRE_BUILT": Box.PRE_BUILT,
        "PICK_AND_MIX": Box.PICK_AND_MIX,
        "FLAVOUR_FORMAT": FLAVOUR_FORMAT,
        "title": box_obj.title,
        "box_obj": box_obj,
        "prebuilds": box_obj.prebuild_options.all(),

    }
    return render(request, "store/box-valentines.html", context)


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
        size_qs = BoxSize.objects.filter(active=True, size=size, special_box=False)

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
                if quantity and int(quantity) > 0:
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
        user_design_id = request.session.get('user_design_id')
        user_design_qs = UserChocolateDesign.objects.filter(active=True, id=user_design_id)
        if user_design_qs.count() == 1:
            cart_entry.user_chocolate_design = user_design_qs.first()
        cart_entry.save()

    return redirect('carts:home')


def add_special_box_to_cart(request):
    form = request.POST
    print(form)

    if form:
        # get box data
        slug = form.get('slug', None)
        flavour_format = form.get(FLAVOUR_FORMAT, None)

        # Check if Size obj exists
        if not slug:
            return redirect('store:home')
        slug_qs = BoxSize.objects.filter(active=True, slug=slug)

        if len(slug_qs) != 1:
            return redirect('store:home')
        box_size_obj = slug_qs.first()

        if flavour_format == Box.PRE_BUILT:
            selected_prebuilts = []
            prebuilds = PreBuildFlavour.objects.filter(active=True)
            for obj in prebuilds:
                selected = form.get(obj.slug, None)
                if selected:
                    selected_prebuilts.append(obj)

            selected_prebuild_slug = form.get("prebuiltFlavor", None)
            selected_prebuild = PreBuildFlavour.objects.filter(active=True, slug=selected_prebuild_slug)

            if selected_prebuild:
                # create box
                new_box = Box(size=box_size_obj, flavour_format=flavour_format)
                new_box.save()
                new_box.selected_prebuilts.set(selected_prebuild)

        elif flavour_format == Box.PICK_AND_MIX:
            flavours = Flavour.objects.active()
            selected_flavours = []
            for obj in flavours:
                quantity = form.get(obj.slug, 0)
                # print(obj.slug, quantity)
                if quantity and int(quantity) > 0:
                    flavour_choice_obj = FlavourChoice(quantity=quantity, flavour=obj)
                    flavour_choice_obj.save()
                    selected_flavours.append(flavour_choice_obj)

            # print(selected_flavours)

            new_box = Box(size=box_size_obj, flavour_format=flavour_format)
            new_box.save()
            new_box.selected_flavours.set(selected_flavours)
        else:
            return redirect('store:home')

        # create entry
        box_quantity = form.get('box_quantity', None)
        cart_entry = CartEntry.objects.new(request, product=new_box, quantity=box_quantity)
        user_design_id = request.session.get('user_design_id')
        user_design_qs = UserChocolateDesign.objects.filter(active=True, id=user_design_id)
        if user_design_qs.count() == 1:
            cart_entry.user_chocolate_design = user_design_qs.first()
        cart_entry.save()

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
