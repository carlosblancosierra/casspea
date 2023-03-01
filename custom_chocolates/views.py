from django.shortcuts import render, redirect

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
    images = []

    for base in obj.base_options.all():
        images.append(base.top_image.url)
        images.append(base.side_image.url)

    for layer in obj.layer1_options.all():
        images.append(layer.top_image.url)
        images.append(layer.side_image.url)

    if obj.layer2_active:
        for layer in obj.layer2_options.all():
            images.append(layer.top_image.url)
            images.append(layer.side_image.url)

    if obj.layer3_active:
        for layer in obj.layer3_options.all():
            images.append(layer.top_image.url)
            images.append(layer.side_image.url)

    context = {
        "obj": obj,
        "image_urls": images
    }

    return render(request, "custom_chocolates/design.html", context)


def box_size_page(request):
    qs = BoxSize.objects.active()
    user_design_id = request.session.get('user_design_id')
    user_design = None

    if user_design_id:
        user_design_qs = UserChocolateDesign.objects.filter(active=True, id=user_design_id)
        if user_design_qs.count() == 1:
            user_design = user_design_qs.first()

    context = {
        "title": "Pick your Box Size",
        "qs": qs,
        "user_design": user_design,
    }

    return render(request, "custom_chocolates/box_size.html", context)


def add_to_cart_page(request, size=None):
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
