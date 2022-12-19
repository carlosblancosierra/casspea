from django.shortcuts import render

from .models import Flavour


# Create your views here.
def home_page(request):
    qs = Flavour.objects.active()

    context = {
        "title": 'Our Flavours',
        "qs": qs,
    }

    return render(request, "flavours/home.html", context)
