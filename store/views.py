from django.shortcuts import render, redirect

from .models import FLAVOURS, PRE_BUILDS_FLAVOURS, PRE_BUILT, PICK_AND_MIX
from flavours.models import PreBuildFlavour


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
        "PRE_BUILT": PRE_BUILT,
        "PICK_AND_MIX": PICK_AND_MIX
    }

    return render(request, "store/box.html", context)


def add_box_to_cart(request):
    form = request.POST
    print(form)
    if form:
        box_quantity = form.get('box_quantity', None)
        size = form.get('size', None)
        format = form.get('format', None)

        if format is PRE_BUILT:
            pre_build = form.get(PRE_BUILT, None)
            # (box_quantity=box_quantity, size=size, format=format, pre_build=pre_build)

        elif format is PICK_AND_MIX:
            pass

    context = {}
    return redirect('store:home')
