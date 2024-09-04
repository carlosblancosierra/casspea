from django.shortcuts import render
from .models import Flavour
from rest_framework import generics
from .serializers import FlavourSerializer

# Create your views here.
def home_page(request):
    qs = Flavour.objects.active()

    split_qs = [qs[i:i + 3] for i in range(0, qs.count(), 3)]
    print(split_qs)

    context = {
        "title": 'Our Flavours',
        "qs": qs,
        "split_qs": split_qs,
    }

    return render(request, "flavours/home.html", context)


class FlavourListView(generics.ListAPIView):
    queryset = Flavour.objects.filter(active=True)
    serializer_class = FlavourSerializer
