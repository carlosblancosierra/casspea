from django.shortcuts import render, redirect, get_object_or_404
import math
from flavours.models import PreBuildFlavour, Flavour, FlavourChoice

from boxes.models import Box, BoxSize
from carts.models import CartEntry

from store.models import FLAVOURS, FLAVOUR_FORMAT

from .models import ChocolateDesignLayer, ChocolateDesign, UserChocolateDesign


# Create your views here.
def test_page(request):
    design = ChocolateDesign.objects.filter(id=1).first()
    background_options = design.background_options.all()
    layer1_options = design.layer1_options.all()
    layer2_options = design.layer1_options.all()
    layer3_options = design.layer1_options.all()

    context = {
        "design": design,
        "background_options": background_options,
        "layer1_options": layer1_options,
        "layer2_options": layer2_options,
        "layer3_options": layer3_options,

    }

    return render(request, "custom_chocolates/test2.html", context)


def design_page(request, slug=None):
    qs = ChocolateDesign.objects.filter(active=True, slug=slug)

    obj = None
    if len(qs) == 1:
        obj = qs.first()

    if request.method == 'POST':
        form = request.POST
        if form:
            base_id = form.get('base_id', None)
            layer1_id = form.get('layer1_id', None)
            layer2_id = form.get('layer2_id', None)
            layer3_id = form.get('layer3_id', None)
            design = obj
            user_design = UserChocolateDesign(
                design=design,
                base_id=base_id,
                layer1_id=layer1_id,
                layer2_id=layer2_id,
                layer3_id=layer3_id,
            )
            if request.user.is_authenticated:
                user_design.user = request.user
            user_design.save()
            request.session['user_design_id'] = user_design.id

            return redirect('custom_chocolates:box_size')
        else:
            errors = form.errors.as_data()
    # x

    context = {
        "obj": obj,
        # "image_urls": images,
        "title": "Personalise your {} design".format(obj.title)
    }

    return render(request, "custom_chocolates/design.html", context)


def box_size_page(request):
    qs = BoxSize.objects.active()

    user_design_id = request.session.get('user_design_id')
    user_design = get_object_or_404(UserChocolateDesign, id=user_design_id)

    context = {
        "title": "Pick your Box Size",
        "qs": qs,
        "user_design": user_design,
    }

    return render(request, "custom_chocolates/box_size.html", context)


def add_to_cart_page(request, size=None):
    user_design_id = request.session.get('user_design_id')
    user_design = get_object_or_404(UserChocolateDesign, id=user_design_id)
    prebuilds = PreBuildFlavour.objects.filter(active=True)
    flavours = Flavour.objects.active()
    box_size_qs = BoxSize.objects.filter(size=size)

    box_obj = None
    if len(box_size_qs) == 1:
        box_obj = box_size_qs.first()

    selects_quantities = range(box_obj.custom_chocolates_min, box_obj.custom_chocolates_min + 30)
    quantity_options = []

    for quantity in selects_quantities:
        max_flavours = math.floor(quantity * box_obj.size / 45)
        if max_flavours == 1:
            text = "{} Boxes, pick 1 flavour".format(quantity)
        elif max_flavours >= len(flavours):
            text = "{} Boxes, You can pick all our {} flavours".format(quantity, len(flavours))
        else:
            text = "{} Boxes, pick up to {} flavours".format(quantity, max_flavours)

        quantity_options.append({
            'quantity': quantity,
            'max_flavours': max_flavours,
            'text': text
        })

    # print(quantity_options)

    context = {
        "size": size,
        "flavours": flavours,
        "prebuilds": prebuilds,
        "PRE_BUILT": Box.PRE_BUILT,
        "PICK_AND_MIX": Box.PICK_AND_MIX,
        "FLAVOUR_FORMAT": FLAVOUR_FORMAT,
        "title": "BOXES",
        "box_obj": box_obj,
        "quantity_options": quantity_options,
        "user_design": user_design,
    }

    return render(request, "custom_chocolates/add_to_cart.html", context)


def add_box_to_cart(request):
    user_design_id = request.session.get('user_design_id')
    user_design = get_object_or_404(UserChocolateDesign, id=user_design_id)
    form = request.POST
    # print(form)

    if form:
        # get box data
        print(form)
        size = form.get('size', None)
        flavour_format = form.get(FLAVOUR_FORMAT, None)

        # Check if Size obj exists
        if not size:
            return redirect('store:home')
        size_qs = BoxSize.objects.filter(active=True, size=size)

        if len(size_qs) != 1:
            return redirect('store:home')
        size_obj = size_qs.first()
        new_box = Box(size=size_obj, flavour_format=flavour_format, custom_design=user_design)
        new_box.save()

        if flavour_format == Box.PRE_BUILT:
            selected_prebuilts = []
            prebuilds = PreBuildFlavour.objects.filter(active=True)
            for obj in prebuilds:
                selected = form.get(obj.slug, None)
                if selected:
                    selected_prebuilts.append(obj)

            # create box
            new_box.selected_prebuilts.set(selected_prebuilts)

        elif flavour_format == Box.PICK_AND_MIX:
            flavours = Flavour.objects.active()
            custom_chocolates_flavours = []
            for obj in flavours:
                selected = form.get(obj.slug, None)
                if selected:
                    custom_chocolates_flavours.append(obj)

            print(custom_chocolates_flavours)

            new_box.custom_chocolates_flavours.set(custom_chocolates_flavours)
        else:
            return redirect('store:home')

        # create entry
        box_quantity = form.get('box_quantity', None)
        cart_entry = CartEntry.objects.new(request, product=new_box, quantity=box_quantity)
        cart_entry.save()

    return redirect('carts:home')


def home_page(request):
    designs = ChocolateDesign.objects.filter(active=True)
    context = {
        "title": "Personalise your Chocolates",
        "designs": designs
    }

    return render(request, "custom_chocolates/home.html", context)
