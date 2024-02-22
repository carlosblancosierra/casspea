from django.shortcuts import render

from .models import Flavour


# Create your views here.
def home_page(request):
    qs = Flavour.objects.all()

    split_qs = [qs[i:i + 3] for i in range(0, qs.count(), 3)]
    print(split_qs)

    context = {
        "title": 'Our Flavours',
        "qs": qs,
        "split_qs": split_qs,
    }

    return render(request, "flavours/home.html", context)
