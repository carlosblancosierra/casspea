from django.shortcuts import render
from .models import Address
from django.http import HttpResponseForbidden


# Create your views here.
def detail_page(request, address_id):
    address = None
    address_qs = Address.objects.filter(id=address_id)

    if len(address_qs) == 1:
        address = address_qs.first()

    if address.user != request.user:
        return HttpResponseForbidden()

    context = {
        "address": address,
    }

    return render(request, "addresses/detail.html", context)


def list_page(request):
    address_qs = Address.objects.filter(user=request.user)

    context = {
        "addresses": address_qs,
    }

    return render(request, "addresses/list.html", context)
